# src/Services/event_handlers/trip_handler.py
"""
Trip Event Handler
==================
Maneja la detección y gestión del ciclo de vida completo de trips (movement/parking).

Extraído de udp.py (Fase 7) para:
- Centralizar lógica compleja de trips (create, close, continue)
- Eliminar side effects (mutación directa de incoming_dict)
- Hacer la lógica testeable sin simular el loop UDP
- Permitir reutilización en otros contextos (HTTP API, batch processing)

Arquitectura:
- Input: Parámetros explícitos (device_id, current_gps, previous_gps, active_trip)
- Output: trip_id (str) o None
- Sin side effects: No modifica parámetros
- Error handling: Captura excepciones y retorna None (GPS se inserta igual)

Funciones:
- calculate_haversine_distance(): Distancia entre dos puntos GPS (fórmula de Haversine)
- calculate_trip_metrics(): Métricas finales de un trip (distancia, duración, velocidad)
- handle_trip_detection(): Orquesta toda la lógica de detección y manejo de trips
"""

from datetime import datetime
from typing import Dict, Any, Optional
from math import radians, sin, cos, sqrt, atan2
from sqlalchemy.orm import Session

# Imports de servicios
from src.Services.trip_detector import trip_detector
from src.Repositories.trip import (
    create_trip,
    get_active_trip_by_device,
    close_trip,
    increment_point_count
)
from src.Repositories.gps_data import get_gps_by_trip_id
from src.Schemas.trip import Trip_create
from src.Core import log_ws


# ==========================================================
# HELPER: CÁLCULO DE DISTANCIA (HAVERSINE)
# ==========================================================

def calculate_haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calcula distancia entre dos puntos GPS usando la fórmula de Haversine.
    
    La fórmula de Haversine calcula la distancia del círculo máximo entre dos puntos
    en una esfera dadas sus latitudes y longitudes. Es suficientemente precisa para
    distancias < 100km.
    
    Fórmula:
        a = sin²(Δlat/2) + cos(lat1) * cos(lat2) * sin²(Δlon/2)
        c = 2 * atan2(√a, √(1−a))
        d = R * c
    
    Args:
        lat1: Latitud del punto 1 (grados decimales)
        lon1: Longitud del punto 1 (grados decimales)
        lat2: Latitud del punto 2 (grados decimales)
        lon2: Longitud del punto 2 (grados decimales)
        
    Returns:
        float: Distancia en metros
        
    Examples:
        >>> # Distancia entre dos puntos cercanos (~111 metros)
        >>> calculate_haversine_distance(10.0, -74.0, 10.001, -74.0)
        111.19...
        
        >>> # Distancia entre el mismo punto (0 metros)
        >>> calculate_haversine_distance(10.5, -74.8, 10.5, -74.8)
        0.0
        
    Notes:
        - Asume la Tierra como esfera perfecta (R = 6371 km)
        - Precisión: ±0.5% para distancias < 100 km
        - Más rápido que geopy (sin dependencias externas)
        - Para distancias > 100 km, considera Vincenty
    """
    # Radio de la Tierra en metros
    R = 6371000
    
    # Convertir grados a radianes
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = sin(delta_lat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance


# ==========================================================
# HELPER: CÁLCULO DE MÉTRICAS DE TRIP
# ==========================================================

def calculate_trip_metrics(db: Session, trip_id: str) -> Dict[str, Any]:
    """
    Calcula métricas finales de un trip antes de cerrarlo.
    
    Este cálculo es CRÍTICO para el cierre correcto de trips. Calcula:
    1. Distancia total: Suma de distancias Haversine entre puntos consecutivos
    2. Duración total: Tiempo desde primer hasta último GPS del trip
    3. Velocidad promedio: (distancia / duración) * 3.6 → km/h
    4. end_time: Timestamp del ÚLTIMO GPS del trip (NO el GPS actual)
    
    ⚠️ IMPORTANTE: end_time
    El end_time retornado es el timestamp del ÚLTIMO GPS que pertenece al trip,
    NO el timestamp del GPS actual que causó el cierre. Esto evita gaps temporales.
    
    Ejemplo del problema:
    - Trip tiene GPS hasta 10:04:58
    - GPS nuevo llega a 10:05:03 y causa cierre del trip
    - ❌ INCORRECTO: end_time = 10:05:03 (gap de 5 segundos)
    - ✅ CORRECTO: end_time = 10:04:58 (último GPS del trip)
    
    Args:
        db: Sesión de SQLAlchemy activa
        trip_id: ID del trip a calcular (ej: "TRIP_20241027_120530_ESP32_001")
        
    Returns:
        dict: Métricas calculadas:
            {
                'distance': float,      # Distancia total en metros
                'duration': float,      # Duración total en segundos
                'avg_speed': float,     # Velocidad promedio en km/h
                'end_time': datetime    # Timestamp del último GPS del trip
            }
            
    Examples:
        >>> metrics = calculate_trip_metrics(db, "TRIP_20241027_120530_ESP32_001")
        >>> metrics
        {
            'distance': 2547.3,
            'duration': 180.5,
            'avg_speed': 50.8,
            'end_time': datetime(2024, 10, 27, 12, 8, 30, tzinfo=timezone.utc)
        }
        
    Edge Cases:
        - Trip sin GPS → {'distance': 0.0, 'duration': 0.0, 'avg_speed': 0.0, 'end_time': None}
        - Trip con 1 GPS → {'distance': 0.0, 'duration': 0.0, 'avg_speed': 0.0, 'end_time': <timestamp>}
        - Trip con 2+ GPS → Métricas calculadas normalmente
        
    Notes:
        - La distancia es acumulativa (suma de segmentos)
        - La velocidad promedio considera toda la duración del trip
        - Si duration == 0, avg_speed = 0 (evita división por cero)
    """
    # Obtener todos los GPS del trip
    gps_points = get_gps_by_trip_id(db, trip_id, include_id=False)
    
    # ========================================
    # CASO 1: Trip sin GPS (no debería pasar, pero defensive)
    # ========================================
    if len(gps_points) < 1:
        return {
            'distance': 0.0,
            'duration': 0.0,
            'avg_speed': 0.0,
            'end_time': None
        }
    
    # ========================================
    # CASO 2: Trip con solo 1 GPS
    # ========================================
    if len(gps_points) == 1:
        # Parse timestamp del único GPS
        single_ts = datetime.fromisoformat(gps_points[0]['Timestamp'].replace('Z', '+00:00'))
        return {
            'distance': 0.0,
            'duration': 0.0,
            'avg_speed': 0.0,
            'end_time': single_ts
        }
    
    # ========================================
    # CASO 3: Trip con 2+ GPS (normal)
    # ========================================
    
    # Calcular distancia total (suma de Haversine entre puntos consecutivos)
    total_distance = 0.0
    for i in range(1, len(gps_points)):
        prev = gps_points[i - 1]
        curr = gps_points[i]
        
        segment_distance = calculate_haversine_distance(
            prev['Latitude'],
            prev['Longitude'],
            curr['Latitude'],
            curr['Longitude']
        )
        total_distance += segment_distance
    
    # Calcular duración (primer GPS hasta último GPS)
    first_ts = datetime.fromisoformat(gps_points[0]['Timestamp'].replace('Z', '+00:00'))
    last_ts = datetime.fromisoformat(gps_points[-1]['Timestamp'].replace('Z', '+00:00'))
    duration = (last_ts - first_ts).total_seconds()
    
    # Calcular velocidad promedio
    if duration > 0:
        avg_speed = (total_distance / duration) * 3.6  # m/s → km/h
    else:
        avg_speed = 0.0
    
    return {
        'distance': total_distance,
        'duration': duration,
        'avg_speed': avg_speed,
        'end_time': last_ts  # ⚠️ CRÍTICO: Timestamp del ÚLTIMO GPS del trip
    }


# ==========================================================
# HANDLER PRINCIPAL: DETECCIÓN Y MANEJO DE TRIPS
# ==========================================================

def handle_trip_detection(
    db: Session,
    device_id: str,
    current_gps: Dict[str, Any],
    previous_gps: Optional[Dict[str, Any]],
    active_trip: Optional[Any]
) -> Optional[str]:
    """
    Maneja detección y gestión del ciclo de vida completo de trips.
    
    Esta es la función más compleja del sistema de trips. Orquesta:
    1. Preparación de datos para trip_detector
    2. Llamada a trip_detector.check_trip()
    3. Ejecución de la acción decidida (create, close, continue)
    4. Logging de eventos de trips
    5. Retorno del trip_id para asociar al GPS
    
    Flujo de decisión:
        INPUT → trip_detector → DECISION → HANDLER EJECUTA → OUTPUT
        
    Las 6 acciones posibles:
        - create_trip: Crear primer trip movement
        - close_and_create_trip: Cerrar parking + crear movement
        - close_and_create_parking: Cerrar movement + crear parking
        - create_parking: Crear parking sin trip anterior
        - continue_trip: Continuar trip activo
        - continue_parking: Continuar parking activo
    
    Arquitectura funcional:
    - NO modifica parámetros (sin side effects)
    - Retorna trip_id (str) o None
    - Error handling interno (no propaga excepciones)
    - GPS se inserta incluso si esto falla (trip_id será None)
    
    Args:
        db: Sesión de SQLAlchemy activa
        device_id: ID del dispositivo (ej: "ESP32_001")
        current_gps: GPS actual con keys:
            - 'Latitude': float
            - 'Longitude': float
            - 'Timestamp': datetime (UTC-aware)
        previous_gps: GPS anterior (dict de get_last_gps_row_by_device) con keys:
            - 'Latitude': float
            - 'Longitude': float
            - 'Timestamp': str (ISO format) ← NOTA: string, no datetime
        active_trip: Trip activo (objeto SQLAlchemy de get_active_trip_by_device)
            - trip_id: str
            - trip_type: 'movement' | 'parking'
            - status: 'active'
            
    Returns:
        str: ID del trip activo/creado (ej: "TRIP_20241027_120530_ESP32_001")
        None: Si no hay trip (error o device inactivo)
        
    Examples:
        >>> # Device arranca (sin trip anterior)
        >>> trip_id = handle_trip_detection(
        ...     db=db,
        ...     device_id="ESP32_001",
        ...     current_gps={'Latitude': 10.5, 'Longitude': -74.8, 'Timestamp': now},
        ...     previous_gps=None,
        ...     active_trip=None
        ... )
        >>> trip_id
        'TRIP_20241027_120530_ESP32_001'
        
        >>> # Device continúa moviéndose
        >>> trip_id = handle_trip_detection(
        ...     db=db,
        ...     device_id="ESP32_001",
        ...     current_gps={'Latitude': 10.51, 'Longitude': -74.81, 'Timestamp': now},
        ...     previous_gps={'Latitude': 10.5, 'Longitude': -74.8, 'Timestamp': '2024-10-27T12:05:25Z'},
        ...     active_trip=<Trip object>
        ... )
        >>> trip_id
        'TRIP_20241027_120530_ESP32_001'  # Mismo trip
        
    Side Effects:
        - Puede crear nuevos trips en la tabla trips
        - Puede cerrar trips activos (UPDATE status='closed')
        - Escribe logs via log_ws.log_from_thread()
        
    Notes:
        - El GPS se inserta SIEMPRE, incluso si esto falla (trip_id = None)
        - previous_gps['Timestamp'] es string ISO → requiere conversión a datetime
        - active_trip puede ser None (device sin trip activo)
        - Error handling retorna None (no propaga excepciones)
    """
    try:
        # ========================================
        # PASO 1: PREPARAR DATOS PARA DETECTOR
        # ========================================
        
        # Extraer trip_id y trip_type del active_trip
        if active_trip:
            active_trip_id = str(active_trip.trip_id)
            current_trip_type = str(active_trip.trip_type)
        else:
            active_trip_id = None
            current_trip_type = None
        
        # ⚠️ CRÍTICO: Convertir timestamp de previous_gps (string → datetime)
        # El repository retorna strings por serialización JSON
        previous_gps_for_detector = None
        if previous_gps:
            prev_ts_str = previous_gps.get('Timestamp')
            if prev_ts_str:
                # Parse ISO timestamp: "2024-10-27T12:05:25.123456Z" → datetime
                prev_ts = datetime.fromisoformat(prev_ts_str.replace('Z', '+00:00'))
            else:
                prev_ts = None
            
            previous_gps_for_detector = {
                'Latitude': previous_gps['Latitude'],
                'Longitude': previous_gps['Longitude'],
                'Timestamp': prev_ts
            }
        
        # ========================================
        # PASO 2: EJECUTAR TRIP DETECTOR
        # ========================================
        
        decision = trip_detector.check_trip(
            device_id=device_id,
            current_gps=current_gps,
            previous_gps=previous_gps_for_detector,
            active_trip_id=active_trip_id,
            current_trip_type=current_trip_type
        )
        
        print(f"[TRIP_HANDLER] Trip decision for {device_id}: {decision['action']} - {decision['reason']}")
        
        # ========================================
        # PASO 3: EJECUTAR ACCIÓN DECIDIDA
        # ========================================
        
        # ACCIÓN 1: Crear nuevo trip (movement)
        if decision['action'] == 'create_trip':
            new_trip = create_trip(db, Trip_create(
                trip_id=decision['trip_id'],
                device_id=device_id,
                trip_type=decision['trip_type'],
                status='active',
                start_time=current_gps['Timestamp'],
                end_time=None,
                start_lat=current_gps['Latitude'],
                start_lon=current_gps['Longitude']
            ))
            log_ws.log_from_thread(
                f"[TRIP] {device_id} started {decision['trip_type'].upper()}: {decision['trip_id']}",
                msg_type="log"
            )
            return str(new_trip.trip_id)
        
        # ACCIÓN 2: Cerrar trip anterior + crear nuevo trip (parking → movement)
        elif decision['action'] == 'close_and_create_trip':
            # Cerrar trip anterior
            if active_trip:
                metrics = calculate_trip_metrics(db, str(active_trip.trip_id))
                close_trip(
                    db,
                    trip_id=str(active_trip.trip_id),
                    end_time=metrics['end_time'],  # ⚠️ CRÍTICO: Último GPS del trip
                    distance=metrics['distance'],
                    duration=metrics['duration'],
                    avg_speed=metrics['avg_speed']
                )
                log_ws.log_from_thread(
                    f"[TRIP] {device_id} closed {str(active_trip.trip_type).upper()}: {str(active_trip.trip_id)} ({metrics['distance']:.0f}m)",
                    msg_type="log"
                )
            
            # Crear nuevo trip
            new_trip = create_trip(db, Trip_create(
                trip_id=decision['trip_id'],
                device_id=device_id,
                trip_type=decision['trip_type'],
                status='active',
                start_time=current_gps['Timestamp'],
                end_time=None,
                start_lat=current_gps['Latitude'],
                start_lon=current_gps['Longitude']
            ))
            log_ws.log_from_thread(
                f"[TRIP] {device_id} started {decision['trip_type'].upper()}: {decision['trip_id']}",
                msg_type="log"
            )
            return str(new_trip.trip_id)
        
        # ACCIÓN 3: Cerrar trip anterior + crear parking (movement → parking)
        elif decision['action'] == 'close_and_create_parking':
            # Cerrar trip anterior
            if active_trip:
                metrics = calculate_trip_metrics(db, str(active_trip.trip_id))
                close_trip(
                    db,
                    trip_id=str(active_trip.trip_id),
                    end_time=metrics['end_time'],  # ⚠️ CRÍTICO: Último GPS del trip
                    distance=metrics['distance'],
                    duration=metrics['duration'],
                    avg_speed=metrics['avg_speed']
                )
                log_ws.log_from_thread(
                    f"[TRIP] {device_id} closed {str(active_trip.trip_type).upper()}: {str(active_trip.trip_id)} ({metrics['distance']:.0f}m)",
                    msg_type="log"
                )
            
            # Crear PARKING
            new_parking = create_trip(db, Trip_create(
                trip_id=decision['trip_id'],
                device_id=device_id,
                trip_type='parking',
                status='active',
                start_time=current_gps['Timestamp'],
                end_time=None,
                start_lat=current_gps['Latitude'],
                start_lon=current_gps['Longitude']
            ))
            log_ws.log_from_thread(
                f"[TRIP] {device_id} started PARKING: {decision['trip_id']}",
                msg_type="log"
            )
            return str(new_parking.trip_id)
        
        # ACCIÓN 4: Crear parking sin trip anterior
        elif decision['action'] == 'create_parking':
            new_parking = create_trip(db, Trip_create(
                trip_id=decision['trip_id'],
                device_id=device_id,
                trip_type='parking',
                status='active',
                start_time=current_gps['Timestamp'],
                end_time=None,
                start_lat=current_gps['Latitude'],
                start_lon=current_gps['Longitude']
            ))
            log_ws.log_from_thread(
                f"[TRIP] {device_id} started PARKING (no prior trip): {decision['trip_id']}",
                msg_type="log"
            )
            return str(new_parking.trip_id)
        
        # ACCIÓN 5: Continuar trip activo (movement)
        elif decision['action'] == 'continue_trip':
            return str(decision['trip_id']) if decision['trip_id'] else None
        
        # ACCIÓN 6: Continuar parking activo
        elif decision['action'] == 'continue_parking':
            return str(decision['trip_id']) if decision['trip_id'] else None
        
        # Catch-all defensivo (no debería llegar aquí)
        else:
            print(f"[TRIP_HANDLER] WARNING: Unknown action '{decision['action']}' for {device_id}")
            return None
    
    except Exception as trip_error:
        # Error en detección de trip - NO debe detener el procesamiento del GPS
        print(f"[TRIP_HANDLER] Trip detection error for {device_id}: {trip_error}")
        import traceback
        traceback.print_exc()
        return None  # GPS se insertará sin trip_id