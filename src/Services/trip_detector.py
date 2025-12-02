# src/Services/trip_detector.py
"""
Trip Detector Service - Core logic for automatic trip segmentation.

Responsibilities:
- Detect trip start/end based on GPS patterns
- Classify trips as 'movement' or 'parking'
- Apply KISS decision matrix (3 questions)
- Accumulate evidence of immobility via GPS counter
- Return structured decisions for UDP service to execute

Key Concepts:
- trip_id is FUNCTIONAL, not semantic (grouping label)
- Stateful: maintains counter per device
- Parking detection: 240 consecutive still GPS (~20 min)

Decision Logic (KISS):
1. First GPS? → Create TRIP
2. Spatial jump (>2km)? → Close + Create TRIP, reset counter
3. Moving (>50m)? 
   - YES → Reset counter, close PARKING if active
   - NO → Increment still counter, and if threshold reached → Create PARKING
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from math import radians, cos, sin, asin, sqrt
from src.Core.config import settings  

# ==========================================================
# 📝 NOTA: Constantes ahora en src/Core/config.py
# ==========================================================
# Para calibrar el sistema de detección de trips:
# - TRIP_JUMP_THRESHOLD_M: Umbral de salto espacial
# - TRIP_STILL_THRESHOLD_M: Umbral de movimiento mínimo
# - TRIP_PARKING_TIME_S: Tiempo quieto para parking
# - TRIP_GPS_INTERVAL_S: Intervalo entre GPS
# ==========================================================


# ==========================================================
# FUNCIÓN: CÁLCULO DE DISTANCIA HAVERSINE
# ==========================================================

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points on Earth.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000
    return c * r


# ==========================================================
# CLASE: TRIP DETECTOR
# ==========================================================

class TripDetector:
    """
    Stateful trip detection engine.
    """
    def __init__(self):
        # Cargar umbrales desde configuración centralizada
        self.jump_threshold_meters = settings.TRIP_JUMP_THRESHOLD_M
        self.still_threshold_meters = settings.TRIP_STILL_THRESHOLD_M
        self.max_time_gap = settings.MAX_TIME_GAP_SECONDS
        
        # Calcular GPS requeridos para parking
        self.still_gps_required = int(
            settings.TRIP_PARKING_TIME_S / settings.TRIP_GPS_INTERVAL_S
        )
        
        # Log de configuración cargada
        print(f"[TRIP_DETECTOR] Initialized with thresholds:")
        print(f"[TRIP_DETECTOR]   - Spatial jump: {self.jump_threshold_meters} m")
        print(f"[TRIP_DETECTOR]   - Still threshold: {self.still_threshold_meters} m")
        print(f"[TRIP_DETECTOR]   - Time gap break: {self.max_time_gap} s")
        print(f"[TRIP_DETECTOR]   - Parking detection: {self.still_gps_required} GPS "
            f"(~{settings.TRIP_PARKING_TIME_S/60:.0f} min)")
        
        # Estado por dispositivo
        self.device_states = {}

    def _get_device_state(self, device_id: str) -> Dict[str, Any]:
        """
        Obtiene o inicializa el estado de un dispositivo.
        """
        if device_id not in self.device_states:
            self.device_states[device_id] = {
                'consecutive_still_gps': 0,
                'last_location': None,
                'last_timestamp': None
            }
        return self.device_states[device_id]

    def _update_device_state(self, device_id: str, **kwargs):
        """
        Actualiza el estado de un dispositivo.
        """
        state = self._get_device_state(device_id)
        state.update(kwargs)

    # ==========================================================
    # FUNCIÓN PRINCIPAL: CHECK_TRIP
    # ==========================================================

    def check_trip(
        self,
        device_id: str,
        current_gps: Dict[str, Any],
        previous_gps: Optional[Dict[str, Any]],
        active_trip_id: Optional[str],
        current_trip_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evalúa un punto GPS y retorna decisión sobre trips/parking.

        Args:
            device_id: Identificador del dispositivo
            current_gps: GPS actual con keys: Latitude, Longitude, Timestamp
            previous_gps: GPS anterior (puede ser None si es el primero)
            active_trip_id: ID del trip actualmente activo (None si no hay)
            current_trip_type: Tipo del trip activo ('movement' o 'parking')

        Returns:
            dict con keys:
                - action: 'create_trip', 'create_parking', 'continue_trip',
                        'continue_parking', 'close_and_create_trip',
                        'close_and_create_parking'
                - trip_type: 'movement' or 'parking'
                - reason: explicación legible
                - trip_id: ID sugerido
                - close_previous: bool
                - consecutive_still_gps: int - contador actualizado
        """

        # Obtener estado del device
        device_state = self._get_device_state(device_id)

        # Extraer datos GPS actual
        current_lat = current_gps['Latitude']
        current_lon = current_gps['Longitude']
        current_time = current_gps['Timestamp']

        # ============================================
        # PREGUNTA 1: ¿Es el primer GPS del dispositivo?
        # ============================================
        if previous_gps is None:
            self._update_device_state(
                device_id,
                consecutive_still_gps=0,
                last_location=(current_lat, current_lon),
                last_timestamp=current_time
            )
            return {
                'action': 'create_trip',
                'trip_type': 'movement',
                'reason': 'First GPS from device (initialization)',
                'trip_id': self._generate_trip_id(device_id, current_time, 'movement'),
                'close_previous': False,
                'consecutive_still_gps': 0
            }

        # Extraer datos del GPS anterior
        prev_lat = previous_gps['Latitude']
        prev_lon = previous_gps['Longitude']

        prev_time = previous_gps.get('Timestamp') 

        # ============================================
        # ✅ NUEVA REGLA: ¿Hay un hueco temporal gigante?
        # ============================================
        if prev_time:
            time_delta = (current_time - prev_time).total_seconds()
            
            if time_delta > self.max_time_gap:
                print(f"[TRIP_DETECTOR] {device_id}: TIME GAP DETECTED - "
                      f"{time_delta:.0f}s > {self.max_time_gap}s. Force Trip Break.")
                
                # Reseteamos estado porque la continuidad se rompió
                self._update_device_state(
                    device_id,
                    consecutive_still_gps=0,
                    last_location=(current_lat, current_lon),
                    last_timestamp=current_time
                )
                
                return {
                    'action': 'close_and_create_trip', # Cerramos lo anterior, iniciamos nuevo
                    'trip_type': 'movement', # Asumimos movimiento al reconectar
                    'reason': f'Time gap detected ({time_delta/60:.0f} min). Forced trip break.',
                    'trip_id': self._generate_trip_id(device_id, current_time, 'movement'),
                    'close_previous': True,
                    'consecutive_still_gps': 0
                }

        # Calcular distancia
        delta_distance = calculate_haversine_distance(
            prev_lat, prev_lon, current_lat, current_lon
        )

        print(f"[TRIP_DETECTOR] {device_id}: Δd={delta_distance:.1f}m, "
            f"contador={device_state['consecutive_still_gps']}")

        # ============================================
        # PREGUNTA 2: ¿Hay salto espacial imposible?
        # ============================================
        if delta_distance > self.jump_threshold_meters:
            print(f"[TRIP_DETECTOR] {device_id}: SPATIAL JUMP DETECTED - "
                f"Δd={delta_distance:.0f}m > {self.jump_threshold_meters}m")
            
            self._update_device_state(
                device_id,
                consecutive_still_gps=0,
                last_location=(current_lat, current_lon),
                last_timestamp=current_time
            )
            return {
                'action': 'close_and_create_trip',
                'trip_type': 'movement',
                'reason': f'Impossible spatial jump ({delta_distance:.0f}m > '
                        f'{self.jump_threshold_meters}m) - GPS noise or device restart',
                'trip_id': self._generate_trip_id(device_id, current_time, 'movement'),
                'close_previous': True,
                'consecutive_still_gps': 0
            }

        # ============================================
        # VALIDACIÓN: Si hay trip activo, debe tener tipo
        # ============================================
        if active_trip_id and current_trip_type is None:
            print(f"[TRIP_DETECTOR] WARNING: {device_id} has active_trip_id but no current_trip_type. Assuming 'movement'")
            current_trip_type = 'movement'

        # ============================================
        # PREGUNTA 3: ¿Se está moviendo?
        # ============================================
        if delta_distance > self.still_threshold_meters:
            # ✅ EN MOVIMIENTO
            print(f"[TRIP_DETECTOR] {device_id}: MOVING - Reset counter to 0")

            self._update_device_state(
                device_id,
                consecutive_still_gps=0,
                last_location=(current_lat, current_lon),
                last_timestamp=current_time
            )

            if current_trip_type == 'parking':
                return {
                    'action': 'close_and_create_trip',
                    'trip_type': 'movement',
                    'reason': f'Movement detected ({delta_distance:.0f}m) - Exiting parking',
                    'trip_id': self._generate_trip_id(device_id, current_time, 'movement'),
                    'close_previous': True,
                    'consecutive_still_gps': 0
                }

            if active_trip_id:
                return {
                    'action': 'continue_trip',
                    'trip_type': 'movement',
                    'reason': f'Normal movement (Δd={delta_distance:.0f}m)',
                    'trip_id': active_trip_id,
                    'close_previous': False,
                    'consecutive_still_gps': 0
                }

            return {
                'action': 'create_trip',
                'trip_type': 'movement',
                'reason': f'Movement detected without active trip (Δd={delta_distance:.0f}m)',
                'trip_id': self._generate_trip_id(device_id, current_time, 'movement'),
                'close_previous': False,
                'consecutive_still_gps': 0
            }

        # ============================================
        # QUIETO (Δd ≤ STILL_THRESHOLD)
        # ============================================
        new_counter = device_state['consecutive_still_gps'] + 1
        print(f"[TRIP_DETECTOR] {device_id}: STILL - Counter: "
            f"{device_state['consecutive_still_gps']} → {new_counter}")

        self._update_device_state(
            device_id,
            consecutive_still_gps=new_counter,
            last_location=(current_lat, current_lon),
            last_timestamp=current_time
        )

        # ¿Se alcanzó el umbral de parking?
        if new_counter >= self.still_gps_required:
            print(f"[TRIP_DETECTOR] {device_id}: PARKING THRESHOLD REACHED "
                f"({new_counter} >= {self.still_gps_required})")

            if current_trip_type == 'movement':
                return {
                    'action': 'close_and_create_parking',
                    'trip_type': 'parking',
                    'reason': f'Vehicle still for {new_counter} GPS '
                            f'({settings.TRIP_PARKING_TIME_S/60:.0f} min) - Creating parking',
                    'trip_id': self._generate_trip_id(device_id, current_time, 'parking'),
                    'close_previous': True,
                    'consecutive_still_gps': new_counter
                }
            
            # Ya es parking o no hay trip activo
            if active_trip_id:
                return {
                    'action': 'continue_parking',
                    'trip_type': 'parking',
                    'reason': f'Continuing parking (still for {new_counter} GPS)',
                    'trip_id': active_trip_id,
                    'close_previous': False,
                    'consecutive_still_gps': new_counter
                }
            else:
                # No hay trip activo, crear parking nuevo
                return {
                    'action': 'create_parking',
                    'trip_type': 'parking',
                    'reason': f'Creating parking after {new_counter} GPS still ({settings.TRIP_PARKING_TIME_S/60:.0f} min)',
                    'trip_id': self._generate_trip_id(device_id, current_time, 'parking'),
                    'close_previous': False,
                    'consecutive_still_gps': new_counter
                }

        # Aún no alcanza umbral
        if active_trip_id:
            return {
                'action': 'continue_trip' if current_trip_type == 'movement' else 'continue_parking',
                'trip_type': current_trip_type or 'movement',
                'reason': f'Still accumulating evidence ({new_counter}/{self.still_gps_required} GPS)',
                'trip_id': active_trip_id,
                'close_previous': False,
                'consecutive_still_gps': new_counter
            }

        return {
            'action': 'create_trip',
            'trip_type': 'movement',
            'reason': f'No active trip, creating movement trip (still count: {new_counter})',
            'trip_id': self._generate_trip_id(device_id, current_time, 'movement'),
            'close_previous': False,
            'consecutive_still_gps': new_counter
        }
    # ==========================================================
    # MÉTODOS AUXILIARES
    # ==========================================================

    def _generate_trip_id(self, device_id: str, timestamp: datetime, trip_type: str) -> str:
        prefix = "TRIP" if trip_type == "movement" else "PARKING"
        date_str = timestamp.strftime("%Y%m%d")
        time_str = timestamp.strftime("%H%M%S")
        safe_device = device_id.replace('-', '').replace('_', '')[:20]
        return f"{prefix}_{date_str}_{safe_device}_{time_str}"

    def get_device_state(self, device_id: str) -> Dict[str, Any]:
        """
        Obtiene el estado actual de un device (para debugging/testing).
        """
        return self._get_device_state(device_id).copy()

    def reset_device_state(self, device_id: str):
        """
        Resetea el estado de un device (útil para testing).
        """
        if device_id in self.device_states:
            del self.device_states[device_id]
            print(f"[TRIP_DETECTOR] State reset for device: {device_id}")


# ==========================================================
# SINGLETON INSTANCE
# ==========================================================

trip_detector = TripDetector()
