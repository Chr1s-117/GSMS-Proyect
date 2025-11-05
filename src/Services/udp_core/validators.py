# src/Services/udp_core/validators.py
"""
Validators Module
=================
Validadores centralizados para dispositivos y schemas de datos.

Extraído de udp.py (Fase 5) para:
- Separar lógica de validación del flujo de control
- Permitir reutilización en otros contextos (HTTP API, WebSocket, etc.)
- Facilitar testing sin simular el loop UDP completo

Arquitectura:
- Validadores retornan None en caso de error (ya logueado)
- El caller decide qué hacer con None (continue, raise, etc.)
- Logging de errores se hace dentro de los validadores

Funciones:
- validate_device(): Verifica device registrado + activo en DB
- validate_gps_schema(): Valida payload GPS con Pydantic
- validate_accel_schema(): Valida payload acelerómetro (non-blocking)
"""

from typing import Optional, Any, Type
from sqlalchemy.orm import Session
from pydantic import ValidationError, BaseModel

# Imports de modelos y logging
from src.Models.device import Device
from src.Core import log_ws


def validate_device(
    db: Session,
    device_id: str,
    sender_ip: str,
    sender_port: int
) -> Optional[Device]:
    """
    Valida que el dispositivo esté registrado y activo en la base de datos.
    
    Realiza dos validaciones críticas de seguridad:
    1. Device existe en la tabla devices (está registrado)
    2. Device tiene IsActive = True (no está deshabilitado)
    
    Args:
        db: Sesión de SQLAlchemy activa
        device_id: ID del dispositivo a validar (ej: "ESP32_001")
        sender_ip: IP del remitente (para logging de seguridad)
        sender_port: Puerto del remitente (para logging de seguridad)
        
    Returns:
        Device: Objeto Device de SQLAlchemy si válido
        None: Si el device no existe o está inactivo (ya logueó el error)
        
    Examples:
        >>> from src.DB.session import SessionLocal
        >>> with SessionLocal() as db:
        ...     device = validate_device(db, "ESP32_001", "192.168.1.100", 9001)
        ...     if device:
        ...         print(f"Device {device.DeviceID} is valid")
        ...     else:
        ...         print("Device validation failed")
        
    Security Notes:
        - Todos los rechazos se loguean con log_ws para auditoría
        - Mensajes de log incluyen IP del remitente para rastreo
        - Devices inactivos pueden reactivarse desde el panel admin
        
    Side Effects:
        - Escribe logs de seguridad via log_ws.log_from_thread()
        - NO modifica la base de datos (solo lectura)
    """
    # PASO 1: Verificar si el device existe en la DB
    device_record = db.query(Device).filter(Device.DeviceID == device_id).first()
    
    if not device_record:
        # Device no registrado - RECHAZO DE SEGURIDAD
        print(f"[VALIDATOR] Unregistered device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
        log_ws.log_from_thread(
            f"[VALIDATOR] SECURITY: Rejected data from unregistered device '{device_id}' (IP: {sender_ip}:{sender_port})",
            msg_type="error"
        )
        return None
    
    # PASO 2: Verificar si el device está activo
    if device_record.IsActive is False:
        # Device deshabilitado - RECHAZO DE SEGURIDAD
        print(f"[VALIDATOR] Inactive device '{device_id}' from {sender_ip}:{sender_port} - REJECTED")
        log_ws.log_from_thread(
            f"[VALIDATOR] SECURITY: Rejected data from inactive device '{device_id}' (IP: {sender_ip}:{sender_port})",
            msg_type="error"
        )
        return None
    
    # ✅ Device válido - retornar objeto
    return device_record


def validate_gps_schema(
    gps_data_class: Type[BaseModel],
    normalized: dict,
    sender_ip: str,
    sender_port: int
) -> Optional[Any]:
    """
    Valida payload GPS normalizado contra schema Pydantic.
    
    Esta validación es CRÍTICA - si falla, el GPS NO se inserta.
    Verifica que todos los campos requeridos estén presentes y tengan
    el tipo correcto según el schema GpsData_create.
    
    Args:
        gps_data_class: Clase Pydantic para validación (ej: GpsData_create)
        normalized: Dict con payload GPS normalizado
        sender_ip: IP del remitente (para logging de errores)
        sender_port: Puerto del remitente (para logging de errores)
        
    Returns:
        GpsData_create | AccelData_create | None: Instancia validada de gps_data_class
        None: Si la validación falla (ya logueó el error)
        
    Examples:
        >>> from src.Schemas.gps_data import GpsData_create
        >>> normalized = {
        ...     'DeviceID': 'ESP32_001',
        ...     'Latitude': 10.5,
        ...     'Longitude': -74.8,
        ...     'Timestamp': datetime.now(timezone.utc)
        ... }
        >>> gps_data = validate_gps_schema(
        ...     GpsData_create,
        ...     normalized,
        ...     "192.168.1.100",
        ...     9001
        ... )
        >>> if gps_data:
        ...     print("GPS data is valid")
        
    Validation Errors:
        - Missing required fields (DeviceID, Latitude, Longitude, Timestamp)
        - Invalid types (string for Latitude, etc.)
        - Out of range values (Latitude > 90, etc.)
        
    Notes:
        - Esta es una validación BLOCKING - el GPS no se procesa si falla
        - El error de Pydantic incluye detalles de qué campo falló
        - Los errores se loguean con print() para debugging local
    """
    try:
        # Intentar crear instancia Pydantic (valida automáticamente)
        gps_data = gps_data_class(**normalized)
        return gps_data
        
    except ValidationError as ve:
        # Error de validación - rechazar payload
        print(f"[VALIDATOR] GPS ValidationError from {sender_ip}:{sender_port}: {ve}")
        print(f"[VALIDATOR] Problematic payload: {normalized}")
        return None


def validate_accel_schema(
    accel_data_class: Type[BaseModel],
    accel_dict: dict,
    device_id: str
) -> Optional[Any]:
    """
    Valida payload de acelerómetro contra schema Pydantic (NON-BLOCKING).
    
    Esta validación es OPCIONAL - si falla, el GPS SE INSERTA DE TODOS MODOS.
    Solo los datos de acelerómetro se descartan si son inválidos.
    
    Diferencia con validate_gps_schema:
    - GPS: BLOCKING (si falla, nada se inserta)
    - Accel: NON-BLOCKING (si falla, solo accel se descarta, GPS se inserta)
    
    Args:
        accel_data_class: Clase Pydantic para validación (ej: AccelData_create)
        accel_dict: Dict con payload acelerómetro aplanado
        device_id: ID del dispositivo (para logging)
        
    Returns:
        AccelData_create | None: Instancia validada de accel_data_class
        None: Si la validación falla (ya logueó el error)
        
    Examples:
        >>> from src.Schemas.accelerometer_data import AccelData_create
        >>> accel_dict = {
        ...     'DeviceID': 'ESP32_001',
        ...     'Timestamp': datetime.now(timezone.utc),
        ...     'ts_start': datetime.now(timezone.utc),
        ...     'ts_end': datetime.now(timezone.utc),
        ...     'rms_x': 0.5,
        ...     'rms_y': 0.3,
        ...     # ... otros campos ...
        ... }
        >>> accel_data = validate_accel_schema(
        ...     AccelData_create,
        ...     accel_dict,
        ...     "ESP32_001"
        ... )
        >>> if accel_data:
        ...     print("Accel data is valid")
        ... else:
        ...     print("Accel data invalid, but GPS will still be inserted")
        
    Validation Errors:
        - Missing required fields (DeviceID, Timestamp, ts_start, ts_end, etc.)
        - Invalid types (string for rms_x, etc.)
        - Invalid datetime formats
        
    Notes:
        - Esta es una validación NON-BLOCKING
        - El GPS se inserta incluso si accel falla
        - Los errores se loguean con log_ws como WARNING (no ERROR)
        - El mensaje indica explícitamente que "GPS will still be inserted"
    """
    try:
        # Intentar crear instancia Pydantic (valida automáticamente)
        accel_data = accel_data_class(**accel_dict)
        return accel_data
        
    except ValidationError as ve:
        # Error de validación - descartar accel pero permitir GPS
        log_ws.log_from_thread(
            f"[VALIDATOR] Accel validation error for {device_id}, GPS will still be inserted: {ve}",
            msg_type="warning"
        )
        print(f"[VALIDATOR] Accel validation failed for {device_id}: {ve}")
        return None


# ==========================================================
# FUTURAS EXTENSIONES (PLACEHOLDER)
# ==========================================================

def validate_obd_schema(
    obd_data_class: Type[BaseModel],
    obd_dict: dict,
    device_id: str
) -> Optional[Any]:
    """
    [FUTURO] Valida payload OBD-II contra schema Pydantic (NON-BLOCKING).
    
    Similar a validate_accel_schema, esta validación será opcional.
    """
    # TODO: Implementar cuando se agregue soporte OBD-II
    raise NotImplementedError("OBD-II validation not yet implemented")


def validate_device_permissions(
    db: Session,
    device_id: str,
    required_permission: str
) -> bool:
    """
    [FUTURO] Valida permisos específicos del dispositivo.
    
    Ejemplo de uso:
    - Verificar si device puede enviar comandos OBD
    - Verificar si device puede actualizar firmware
    - Verificar si device tiene acceso a geocercas premium
    
    Args:
        db: Sesión de SQLAlchemy
        device_id: ID del dispositivo
        required_permission: Permiso requerido (ej: "obd_commands")
        
    Returns:
        bool: True si tiene el permiso, False en caso contrario
    """
    # TODO: Implementar sistema de permisos granular
    raise NotImplementedError("Permission validation not yet implemented")