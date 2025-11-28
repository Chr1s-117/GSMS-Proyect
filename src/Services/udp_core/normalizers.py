# src/Services/udp_core/normalizers.py
"""
GPS Data Normalizers Module
============================
Normaliza payloads GPS crudos del UDP al schema interno de Pydantic.

Extraído de udp.py (Fase 3) para:
- Reutilización en múltiples fuentes de datos (UDP, HTTP, MQTT)
- Testing unitario de transformaciones de datos
- Mantenibilidad de reglas de mapeo centralizadas

Funciones:
- coerce_number(): Convierte strings numéricos a float
- normalize_timestamp(): UNIX seconds/ms → datetime UTC
- normalize_gps_payload(): Orquesta mapeo + filtrado + coerción
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union


# ==========================================================
# CONSTANTES DE MAPEO
# ==========================================================

ALLOWED_KEYS = {
    "DeviceID",
    "Latitude",
    "Longitude",
    "Altitude",
    "Accuracy",
    "Timestamp"
}
"""
Campos permitidos en el payload GPS normalizado.
Cualquier otro campo será filtrado.
"""

KEY_MAP = {
    # Device ID variants
    "device_id": "DeviceID",
    "deviceId": "DeviceID",
    "deviceid": "DeviceID",
    "device": "DeviceID",
    "DeviceID": "DeviceID",
    
    # GPS coordinate variants
    "latitude": "Latitude",
    "lat": "Latitude",
    "Latitude": "Latitude",
    
    "longitude": "Longitude",
    "lon": "Longitude",
    "lng": "Longitude",
    "Longitude": "Longitude",
    
    "altitude": "Altitude",
    "alt": "Altitude",
    "Altitude": "Altitude",
    
    "accuracy": "Accuracy",
    "acc": "Accuracy",
    "Accuracy": "Accuracy",
    
    # Timestamp variants
    "timestamp": "Timestamp",
    "time": "Timestamp",
    "timeStamp": "Timestamp",
    "Timestamp": "Timestamp",
}
"""
Mapeo de nombres de campos alternativos al nombre canónico.
Permite recibir 'deviceId', 'device_id', etc. y normalizarlos a 'DeviceID'.
"""


# ==========================================================
# FUNCIONES DE BAJO NIVEL
# ==========================================================

def coerce_number(value: Any) -> Union[float, int, str, None]:
    """
    Convierte strings numéricos a float, maneja null/empty.
    
    Reglas de conversión:
    - None → None
    - int/float → mantiene como está
    - "" → None
    - "null" (case-insensitive) → None
    - "3,14" → 3.14 (reemplaza coma por punto)
    - "42" → 42.0
    - Cualquier otro string no numérico → mantiene como string
    
    Args:
        value: Valor a convertir (puede ser cualquier tipo)
        
    Returns:
        float | int | str | None: Número convertido, None, o string original
        
    Examples:
        >>> coerce_number("3.14")
        3.14
        >>> coerce_number("3,14")
        3.14
        >>> coerce_number("null")
        None
        >>> coerce_number("")
        None
        >>> coerce_number(42)
        42
        >>> coerce_number("not_a_number")
        'not_a_number'
    """
    if value is None:
        return None
    
    if isinstance(value, (int, float)):
        return value
    
    if isinstance(value, str):
        v = value.strip()
        
        # Manejar strings vacíos o "null"
        if v == "" or v.lower() == "null":
            return None
        
        # Reemplazar coma decimal europea por punto
        v = v.replace(",", ".")
        
        try:
            return float(v)
        except ValueError:
            # No es convertible a número, retornar original
            return value
    
    return value


def normalize_timestamp(ts_value: Any) -> datetime:
    """
    Normaliza timestamp a datetime UTC-aware.
    
    Soporta múltiples formatos:
    - datetime objects (con o sin timezone)
    - UNIX timestamp en segundos (1730000000)
    - UNIX timestamp en milisegundos (1730000000000)
    - Strings numéricos de cualquiera de los anteriores
    
    Heurística para distinguir segundos vs milisegundos:
    - Si timestamp > 10^10 (10,000,000,000) → asume milisegundos
    - Ejemplo: 1730000000 (segundos) vs 1730000000000 (milisegundos)
    
    Args:
        ts_value: Timestamp en cualquier formato soportado
        
    Returns:
        datetime: UTC-aware datetime object
        
    Raises:
        ValueError: Si el formato no es reconocible
        
    Examples:
        >>> normalize_timestamp(1730000000)  # Segundos
        datetime.datetime(2024, 10, 27, 4, 53, 20, tzinfo=datetime.timezone.utc)
        
        >>> normalize_timestamp(1730000000000)  # Milisegundos
        datetime.datetime(2024, 10, 27, 4, 53, 20, tzinfo=datetime.timezone.utc)
        
        >>> normalize_timestamp("1730000000")  # String numérico
        datetime.datetime(2024, 10, 27, 4, 53, 20, tzinfo=datetime.timezone.utc)
        
        >>> from datetime import datetime, timezone
        >>> dt = datetime(2024, 10, 27, tzinfo=timezone.utc)
        >>> normalize_timestamp(dt)
        datetime.datetime(2024, 10, 27, 0, 0, tzinfo=datetime.timezone.utc)
    """
    # Ya es datetime
    if isinstance(ts_value, datetime):
        # Asegurar que tenga timezone UTC
        return ts_value if ts_value.tzinfo else ts_value.replace(tzinfo=timezone.utc)
    
    # Convertir a float
    try:
        ts_float = float(ts_value)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid timestamp format: {ts_value}") from e
    
    # Heurística: timestamps > 10^10 son milisegundos
    # Razón: UNIX epoch en segundos alcanzó 10^10 en septiembre 2001
    # Los timestamps actuales en segundos están en ~1.7×10^9
    # Los timestamps en milisegundos están en ~1.7×10^12
    if ts_float > 10_000_000_000:
        ts_float = ts_float / 1000.0
    
    return datetime.fromtimestamp(ts_float, tz=timezone.utc)


# ==========================================================
# FUNCIÓN DE ALTO NIVEL
# ==========================================================

def normalize_gps_payload(raw_payload: Any) -> Dict[str, Any]:
    """
    Normaliza payload GPS del formato UDP al schema interno.
    
    Proceso de normalización:
    1. Maneja payloads envueltos en objeto single-key
    2. Mapea claves alternativas (deviceId → DeviceID)
    3. Filtra campos no permitidos (solo ALLOWED_KEYS)
    4. Convierte números en strings a float
    
    Args:
        raw_payload: Payload crudo del UDP (dict o nested dict)
        
    Returns:
        dict: Payload normalizado con claves canónicas
        
    Examples:
        >>> raw = {
        ...     "deviceId": "ESP32_001",
        ...     "lat": "10.5",
        ...     "lon": "-74.8",
        ...     "timestamp": 1730000000,
        ...     "extra_field": "ignored"
        ... }
        >>> normalize_gps_payload(raw)
        {
            'DeviceID': 'ESP32_001',
            'Latitude': 10.5,
            'Longitude': -74.8,
            'Timestamp': 1730000000
        }
        
        >>> # Payload envuelto (común en algunos dispositivos)
        >>> wrapped = {"gps": {"deviceId": "ESP32_001", "lat": 10.5}}
        >>> normalize_gps_payload(wrapped)
        {'DeviceID': 'ESP32_001', 'Latitude': 10.5}
        
    Notes:
        - El timestamp NO es normalizado aquí (se hace después con normalize_timestamp)
        - Campos no reconocidos son silenciosamente descartados
        - Si raw_payload no es dict, retorna dict vacío
    """
    # Manejar payloads envueltos en objeto single-key
    # Ejemplo: {"gps": {"DeviceID": "...", "Latitude": ...}}
    if isinstance(raw_payload, dict) and len(raw_payload) == 1:
        only_key = next(iter(raw_payload))
        candidate = raw_payload[only_key] if isinstance(raw_payload[only_key], dict) else raw_payload
    else:
        candidate = raw_payload if isinstance(raw_payload, dict) else {}
    
    normalized: Dict[str, Any] = {}
    
    for k, v in candidate.items():
        # Mapear clave alternativa a nombre canónico
        # Ejemplo: "deviceId" → "DeviceID"
        mapped = KEY_MAP.get(k, KEY_MAP.get(k.lower(), k))
        
        # Filtrar: solo permitir campos en ALLOWED_KEYS
        if mapped in ALLOWED_KEYS:
            normalized[mapped] = coerce_number(v)
    
    return normalized