# src/Services/event_handlers/geofence_handler.py
"""
Geofence Event Handler
======================
Maneja la detección y logging de eventos de geocercas.

Extraído de udp.py (Fase 6) para:
- Eliminar side effects (mutación directa de incoming_dict)
- Hacer la lógica testeable sin simular el loop UDP
- Permitir reutilización en otros contextos (HTTP API, batch processing)
- Centralizar lógica de EXIT artificial

Arquitectura:
- Input: Parámetros explícitos (device_id, lat, lon, timestamp, etc.)
- Output: Dict con campos de geocerca (nunca None, siempre dict válido)
- Sin side effects: No modifica parámetros ni variables globales
- Error handling: Captura excepciones y retorna defaults seguros

Funciones:
- handle_geofence_detection(): Detecta geocercas y maneja eventos ENTRY/EXIT
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

# Imports de servicios
from src.Services.geofence_detector import geofence_detector
from src.Repositories.gps_data import created_gps_data
from src.Schemas.gps_data import GpsData_create
from src.Core import log_ws


def handle_geofence_detection(
    db: Session,
    device_id: str,
    latitude: float,
    longitude: float,
    altitude: Optional[float],
    accuracy: Optional[float],
    timestamp: datetime,
    previous_gps: Optional[dict]
) -> Dict[str, Any]:
    """
    Maneja detección de geocercas y eventos de transición (ENTRY/EXIT).
    
    Flujo de detección:
    1. Consulta geofence_detector para verificar si el punto está en alguna geocerca
    2. Si es ENTRY y había geocerca anterior → crea EXIT artificial 1μs antes
    3. Actualiza campos de geocerca para el GPS actual
    4. Loguea solo eventos de transición (ENTRY/EXIT, no "inside")
    
    Arquitectura funcional:
    - NO modifica parámetros (sin side effects)
    - Retorna dict con campos de geocerca
    - Siempre retorna dict válido (incluso en error)
    - Error handling interno (no propaga excepciones)
    
    Args:
        db: Sesión de SQLAlchemy activa
        device_id: ID del dispositivo
        latitude: Latitud actual (grados decimales)
        longitude: Longitud actual (grados decimales)
        altitude: Altitud actual en metros (opcional)
        accuracy: Precisión GPS en metros (opcional)
        timestamp: Timestamp UTC del GPS actual
        previous_gps: GPS anterior del dispositivo (dict de get_last_gps_row_by_device)
                     Debe contener: CurrentGeofenceID, CurrentGeofenceName
        
    Returns:
        dict: Campos de geocerca para agregar al GPS:
            {
                'CurrentGeofenceID': int | None,
                'CurrentGeofenceName': str | None,
                'GeofenceEventType': 'entry' | 'exit' | 'inside' | None
            }
        
    Examples:
        >>> # Device entra a geocerca "Warehouse A"
        >>> result = handle_geofence_detection(
        ...     db=db,
        ...     device_id="ESP32_001",
        ...     latitude=10.5,
        ...     longitude=-74.8,
        ...     altitude=100.0,
        ...     accuracy=5.0,
        ...     timestamp=datetime.now(timezone.utc),
        ...     previous_gps=None  # Primera vez
        ... )
        >>> result
        {
            'CurrentGeofenceID': 42,
            'CurrentGeofenceName': 'Warehouse A',
            'GeofenceEventType': 'entry'
        }
        
        >>> # Device fuera de geocercas
        >>> result = handle_geofence_detection(...)
        >>> result
        {
            'CurrentGeofenceID': None,
            'CurrentGeofenceName': None,
            'GeofenceEventType': None
        }
        
    Side Effects:
        - Puede crear registro GPS de EXIT artificial en la DB (si corresponde)
        - Escribe logs via log_ws.log_from_thread() para eventos ENTRY/EXIT
        
    Notes:
        - EXIT artificial se crea 1 microsegundo antes del ENTRY para mantener orden
        - Solo se loguean eventos ENTRY/EXIT (no "inside" para evitar spam)
        - Si geofence_detector falla, retorna dict con valores None (failsafe)
        - El registro EXIT artificial tiene las mismas coordenadas que el ENTRY
          (porque el dispositivo salió "instantáneamente" de la geocerca anterior)
    """
    # Resultado por defecto (usado en caso de error o sin geocerca)
    result: Dict[str, Any] = {
        'CurrentGeofenceID': None,
        'CurrentGeofenceName': None,
        'GeofenceEventType': None
    }
    
    try:
        # ========================================
        # PASO 1: DETECTAR GEOCERCA ACTUAL
        # ========================================
        geofence_info = geofence_detector.check_point(
            db=db,
            device_id=device_id,
            lat=latitude,
            lon=longitude,
            timestamp=timestamp
        )
        
        # Si no está en ninguna geocerca, retornar defaults
        if not geofence_info:
            return result
        
        # ========================================
        # PASO 2: MANEJO DE EXIT ARTIFICIAL
        # ========================================
        # Si es ENTRY y el device estaba en otra geocerca antes,
        # crear un registro EXIT de la geocerca anterior
        if (
            geofence_info['event_type'] == 'entry' and 
            previous_gps and 
            previous_gps.get('CurrentGeofenceID')
        ):
            # Crear registro EXIT artificial 1 μs antes del ENTRY
            exit_dict = {
                'DeviceID': device_id,
                'Latitude': latitude,
                'Longitude': longitude,
                'Altitude': altitude,
                'Accuracy': accuracy,
                'Timestamp': timestamp - timedelta(microseconds=1),
                'CurrentGeofenceID': str(previous_gps['CurrentGeofenceID']),
                'CurrentGeofenceName': previous_gps['CurrentGeofenceName'],
                'GeofenceEventType': 'exit'
            }
            
            # Insertar EXIT en DB
            created_gps_data(db, GpsData_create(**exit_dict))
            
            # Log del EXIT
            log_ws.log_from_thread(
                f"[GEOFENCE] {device_id} EXITED {previous_gps['CurrentGeofenceName']}",
                msg_type="log"
            )
        
        # ========================================
        # PASO 3: ACTUALIZAR CAMPOS DEL GPS ACTUAL
        # ========================================
        result['CurrentGeofenceID'] = str(geofence_info['id']) if geofence_info['id'] is not None else None
        result['CurrentGeofenceName'] = geofence_info['name']
        result['GeofenceEventType'] = geofence_info['event_type']
        
        # ========================================
        # PASO 4: LOGGING CONDICIONAL
        # ========================================
        # Solo loguear ENTRY/EXIT (no "inside" para evitar spam)
        if geofence_info['event_type'] in ('entry', 'exit'):
            action = "ENTERED" if geofence_info['event_type'] == 'entry' else "EXITED"
            
            # Determinar nombre de la geocerca
            if geofence_info['event_type'] == 'exit':
                # Para EXIT, usar el nombre del GPS anterior si existe
                geo_name = previous_gps.get('CurrentGeofenceName', 'Unknown Zone') if previous_gps else 'Unknown Zone'
            else:
                # Para ENTRY, usar el nombre de geofence_info
                geo_name = geofence_info.get('name', 'Unknown')
            
            log_ws.log_from_thread(
                f"[GEOFENCE] {device_id} {action} {geo_name}",
                msg_type="log"
            )
        
    except Exception as geo_error:
        # Error en detección de geocerca - no debe detener el procesamiento del GPS
        print(f"[GEOFENCE_HANDLER] Geofence detection error for {device_id}: {geo_error}")
        # result ya tiene valores None por defecto
    
    return result