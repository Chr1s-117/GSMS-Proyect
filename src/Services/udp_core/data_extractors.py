# src/Services/udp_core/data_extractors.py
"""
Data Extractors Module
======================
Extractores de datos específicos para diferentes tipos de sensores.

Extraído de udp.py (Fase 4) para:
- Separar lógica especializada por tipo de sensor
- Permitir extensión futura (OBD-II, temperatura, etc.)
- Mantener normalizers.py genérico (solo GPS)

Funciones:
- extract_accel_data(): Extrae y aplana datos de acelerómetro del payload UDP

Futuras extensiones posibles:
- extract_obd_data(): Datos de diagnóstico del vehículo
- extract_temp_data(): Datos de sensores de temperatura
- extract_fuel_data(): Datos de consumo de combustible
"""

from datetime import datetime
from typing import Optional, Dict, Any

# ✅ Import relativo - indica que está en el mismo paquete (udp_core)
from .normalizers import normalize_timestamp


def extract_accel_data(
    raw_payload: dict,
    device_id: str,
    gps_timestamp: datetime
) -> Optional[Dict[str, Any]]:
    """
    Extrae y aplana datos de acelerómetro del payload UDP.
    
    Transforma estructura anidada JSON en estructura plana compatible
    con el schema Pydantic AccelData_create.
    
    Estructura de entrada esperada:
    ```json
    {
        "accel": {
            "ts_start": 1730000000,        // UNIX timestamp (segundos o milisegundos)
            "ts_end": 1730000001,          // UNIX timestamp (segundos o milisegundos)
            "rms": {                        // Root Mean Square (valores RMS)
                "x": 0.5,
                "y": 0.3,
                "z": 0.8,
                "mag": 1.0                  // Magnitud total
            },
            "max": {                        // Valores máximos en la ventana
                "x": 1.2,
                "y": 0.9,
                "z": 1.5,
                "mag": 2.1
            },
            "peaks_count": 5,               // Número de picos detectados
            "sample_count": 250,            // Muestras tomadas (típicamente 250 @ 250Hz)
            "flags": 0                      // Flags de estado (0 = normal)
        }
    }
    ```
    
    Estructura de salida (aplanada):
    ```python
    {
        'DeviceID': 'ESP32_001',
        'Timestamp': datetime(2024, 10, 27, 4, 53, 20, tzinfo=timezone.utc),
        'ts_start': datetime(2024, 10, 27, 4, 53, 20, tzinfo=timezone.utc),
        'ts_end': datetime(2024, 10, 27, 4, 53, 21, tzinfo=timezone.utc),
        'rms_x': 0.5,
        'rms_y': 0.3,
        'rms_z': 0.8,
        'rms_mag': 1.0,
        'max_x': 1.2,
        'max_y': 0.9,
        'max_z': 1.5,
        'max_mag': 2.1,
        'peaks_count': 5,
        'sample_count': 250,
        'flags': 0
    }
    ```
    
    Args:
        raw_payload: Payload UDP completo (debe contener clave 'accel')
        device_id: ID del dispositivo que envió los datos
        gps_timestamp: Timestamp del GPS asociado (para el campo Timestamp)
        
    Returns:
        dict | None: Diccionario con 16 campos aplanados, o None si:
            - No existe la clave 'accel' en raw_payload
            - Faltan campos requeridos (ts_start, ts_end)
            - Error al parsear timestamps
            - Error al convertir valores numéricos
            
    Examples:
        >>> raw = {
        ...     "DeviceID": "ESP32_001",
        ...     "Latitude": 10.5,
        ...     "accel": {
        ...         "ts_start": 1730000000,
        ...         "ts_end": 1730000001,
        ...         "rms": {"x": 0.5, "y": 0.3, "z": 0.8, "mag": 1.0},
        ...         "max": {"x": 1.2, "y": 0.9, "z": 1.5, "mag": 2.1},
        ...         "peaks_count": 5,
        ...         "sample_count": 250,
        ...         "flags": 0
        ...     }
        ... }
        >>> from datetime import datetime, timezone
        >>> gps_ts = datetime(2024, 10, 27, tzinfo=timezone.utc)
        >>> result = extract_accel_data(raw, "ESP32_001", gps_ts)
        >>> result['DeviceID']
        'ESP32_001'
        >>> result['rms_x']
        0.5
        >>> isinstance(result['ts_start'], datetime)
        True
        
    Notes:
        - Los timestamps (ts_start, ts_end) son normalizados automáticamente
          usando normalize_timestamp() (soporta segundos y milisegundos)
        - Si faltan campos anidados (rms.x, max.y, etc.), se usa 0.0 por defecto
        - peaks_count y sample_count tienen valores por defecto (0 y 250)
        - La función NO valida contra el schema Pydantic (eso se hace después)
        - Todos los errores de parsing se capturan y retornan None
    """
    # Verificar existencia de datos de acelerómetro
    accel = raw_payload.get('accel')
    if not accel:
        return None
    
    try:
        # ========================================
        # PASO 1: NORMALIZAR TIMESTAMPS
        # ========================================
        # Convertir UNIX timestamps (segundos o milisegundos) a datetime UTC
        ts_start = normalize_timestamp(accel['ts_start'])
        ts_end = normalize_timestamp(accel['ts_end'])
        
        # ========================================
        # PASO 2: EXTRAER ESTRUCTURAS ANIDADAS
        # ========================================
        # RMS (Root Mean Square) - valores estadísticos de vibración
        rms = accel.get('rms', {})
        
        # MAX - picos máximos en la ventana de muestreo
        max_vals = accel.get('max', {})
        
        # ========================================
        # PASO 3: APLANAR ESTRUCTURA
        # ========================================
        # Convertir estructura anidada a flat dict con 16 campos
        return {
            # Metadatos
            'DeviceID': device_id,
            'Timestamp': gps_timestamp,
            
            # Timestamps de ventana
            'ts_start': ts_start,
            'ts_end': ts_end,
            
            # RMS por eje (4 campos)
            'rms_x': float(rms.get('x', 0.0)),
            'rms_y': float(rms.get('y', 0.0)),
            'rms_z': float(rms.get('z', 0.0)),
            'rms_mag': float(rms.get('mag', 0.0)),
            
            # Máximos por eje (4 campos)
            'max_x': float(max_vals.get('x', 0.0)),
            'max_y': float(max_vals.get('y', 0.0)),
            'max_z': float(max_vals.get('z', 0.0)),
            'max_mag': float(max_vals.get('mag', 0.0)),
            
            # Métricas agregadas
            'peaks_count': int(accel.get('peaks_count', 0)),
            'sample_count': int(accel.get('sample_count', 250)),  # Típicamente 250 @ 250Hz
            
            # Estado
            'flags': int(accel.get('flags', 0))  # 0 = normal, otros = errores
        }
    
    except (KeyError, ValueError, TypeError) as e:
        # Errores posibles:
        # - KeyError: falta ts_start o ts_end (requeridos)
        # - ValueError: timestamp inválido, conversión a float/int falló
        # - TypeError: tipo de dato inesperado (ej. None donde se espera dict)
        print(f"[DATA_EXTRACTOR] Error extracting accel data: {e}")
        return None


# ==========================================================
# FUTURAS EXTENSIONES (PLACEHOLDER)
# ==========================================================

def extract_obd_data(
    raw_payload: dict,
    device_id: str,
    gps_timestamp: datetime
) -> Optional[Dict[str, Any]]:
    """
    [FUTURO] Extrae datos OBD-II del payload UDP.
    
    Estructura esperada:
    {
        "obd": {
            "rpm": 2500,
            "speed": 80,
            "fuel_level": 75.5,
            "engine_temp": 90,
            "dtc_codes": []
        }
    }
    """
    # TODO: Implementar cuando se agregue soporte OBD-II
    raise NotImplementedError("OBD-II extraction not yet implemented")


def extract_temp_data(
    raw_payload: dict,
    device_id: str,
    gps_timestamp: datetime
) -> Optional[Dict[str, Any]]:
    """
    [FUTURO] Extrae datos de sensores de temperatura del payload UDP.
    
    Estructura esperada:
    {
        "temp": {
            "ambient": 25.5,
            "engine": 95.0,
            "cabin": 22.0
        }
    }
    """
    # TODO: Implementar cuando se agregue soporte de temperatura
    raise NotImplementedError("Temperature extraction not yet implemented")