# src/Repositories/accelerometer_data.py

from sqlalchemy.orm import Session
from src.Models.accelerometer_data import AccelerometerData
from src.Schemas.accelerometer_data import AccelData_create, AccelData_update
from src.Models.gps_data import GPS_data
from typing import List, Optional, Any
from datetime import datetime


# ==========================================================
# CRUD BÁSICO
# ==========================================================

def create_accel_data(db: Session, accel_data: AccelData_create) -> AccelerometerData:
    """
    Crea un nuevo registro de acelerómetro.
    
    Args:
        db: Session SQLAlchemy
        accel_data: Schema validado
        
    Returns:
        AccelerometerData: Registro insertado
        
    Raises:
        IntegrityError: Si viola unique constraint (DeviceID, Timestamp)
    """
    new_accel = AccelerometerData(**accel_data.model_dump(exclude_unset=True))
    db.add(new_accel)
    db.commit()
    db.refresh(new_accel)
    return new_accel


def get_accel_by_id(db: Session, accel_id: int) -> Optional[AccelerometerData]:
    """Obtiene un registro por su ID interno."""
    return db.query(AccelerometerData).filter(AccelerometerData.id == accel_id).first()


def update_accel_data(
    db: Session, 
    accel_id: int, 
    accel_data: AccelData_update
) -> Optional[AccelerometerData]:
    """
    Actualiza un registro existente.
    
    Nota: Normalmente los datos de acelerómetro son inmutables,
    pero esta función permite correcciones si es necesario.
    """
    db_accel = get_accel_by_id(db, accel_id)
    
    if not db_accel:
        return None
    
    update_dict = accel_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if hasattr(db_accel, key):
            setattr(db_accel, key, value)
    
    db.commit()
    db.refresh(db_accel)
    return db_accel


def delete_accel_data(db: Session, accel_id: int) -> bool:
    """
    Elimina un registro de acelerómetro.
    
    Returns:
        True si se eliminó, False si no existía
    """
    db_accel = get_accel_by_id(db, accel_id)
    
    if not db_accel:
        return False
    
    db.delete(db_accel)
    db.commit()
    return True

# ==========================================================
# CONSULTAS POR DISPOSITIVO
# ==========================================================

def get_all_accel_by_device(
    db: Session, 
    device_id: str
) -> List[AccelerometerData]:
    """
    Obtiene TODOS los registros de acelerómetro de un dispositivo.
    
    Warning: Puede retornar muchos registros si el device tiene
    mucho histórico. Usar con precaución.
    """
    return (
        db.query(AccelerometerData)
        .filter(AccelerometerData.DeviceID == device_id)
        .order_by(AccelerometerData.Timestamp.asc())
        .all()
    )


def get_last_accel_by_device(
    db: Session, 
    device_id: str
) -> Optional[AccelerometerData]:
    """
    Obtiene el registro más reciente de un dispositivo.
    Equivalente a get_last_gps_row_by_device() pero para accel.
    """
    return (
        db.query(AccelerometerData)
        .filter(AccelerometerData.DeviceID == device_id)
        .order_by(AccelerometerData.id.desc())
        .first()
    )


def get_oldest_accel_by_device(
    db: Session, 
    device_id: str
) -> Optional[AccelerometerData]:
    """
    Obtiene el registro más antiguo de un dispositivo.
    """
    return (
        db.query(AccelerometerData)
        .filter(AccelerometerData.DeviceID == device_id)
        .order_by(AccelerometerData.id.asc())
        .first()
    )


def get_accel_by_device_timestamp(
    db: Session, 
    device_id: str, 
    timestamp: datetime
) -> Optional[AccelerometerData]:
    """
    Busca un registro específico por (DeviceID, Timestamp).
    Útil para verificar duplicados o hacer JOINs manuales con GPS.
    """
    return (
        db.query(AccelerometerData)
        .filter(
            AccelerometerData.DeviceID == device_id,
            AccelerometerData.Timestamp == timestamp
        )
        .first()
    )
    
# ==========================================================
# CONSULTAS POR RANGO TEMPORAL
# ==========================================================

def get_accel_in_range_by_device(
    db: Session,
    device_id: str,
    start_time: datetime,
    end_time: datetime
) -> List[AccelerometerData]:
    """
    Obtiene datos de acelerómetro en un rango de tiempo para un device.
    Equivalente a get_gps_data_in_range_by_device().
    
    Args:
        device_id: ID del dispositivo
        start_time: Inicio del rango (inclusive, UTC)
        end_time: Fin del rango (inclusive, UTC)
    """
    return (
        db.query(AccelerometerData)
        .filter(
            AccelerometerData.DeviceID == device_id,
            AccelerometerData.Timestamp >= start_time,
            AccelerometerData.Timestamp <= end_time
        )
        .order_by(AccelerometerData.Timestamp.asc())
        .all()
    )


def get_accel_in_range(
    db: Session,
    start_time: datetime,
    end_time: datetime
) -> List[AccelerometerData]:
    """
    [LEGACY] Obtiene datos de acelerómetro de TODOS los devices en un rango.
    
    Warning: Solo para exportaciones globales o análisis administrativos.
    Para queries específicos, usar get_accel_in_range_by_device().
    """
    return (
        db.query(AccelerometerData)
        .filter(
            AccelerometerData.Timestamp >= start_time,
            AccelerometerData.Timestamp <= end_time
        )
        .order_by(AccelerometerData.Timestamp.asc())
        .all()
    )
# ==========================================================
# UTILIDADES
# ==========================================================

def device_has_accel_data(db: Session, device_id: str) -> bool:
    """
    Verifica si un dispositivo tiene al menos un registro de acelerómetro.
    """
    count = (
        db.query(AccelerometerData)
        .filter(AccelerometerData.DeviceID == device_id)
        .limit(1)
        .count()
    )
    return count > 0


def count_accel_records(
    db: Session, 
    device_id: Optional[str] = None
) -> int:
    """
    Cuenta registros de acelerómetro.
    
    Args:
        device_id: Si se provee, cuenta solo ese device. 
                   Si es None, cuenta todos los registros.
    """
    query = db.query(AccelerometerData)
    
    if device_id:
        query = query.filter(AccelerometerData.DeviceID == device_id)
    
    return query.count()


def get_all_devices_with_accel(db: Session) -> List[str]:
    """
    Obtiene lista de DeviceIDs que tienen datos de acelerómetro.
    Equivalente a get_all_devices() de GPS.
    """
    result = db.query(AccelerometerData.DeviceID).distinct().all()
    return [row[0] for row in result]

# ==========================================================
# 🆕 FASE 2: AGREGACIÓN POR TRIP
# ==========================================================

def get_accel_map_for_trip(
    db: Session,
    trip_id: str
) -> dict[str, dict[str, Any]]:
    """
    Get accelerometer data for a trip as timestamp-keyed map for efficient JOIN.
    
    Returns a dictionary mapping GPS timestamps to accelerometer data.
    This enables O(1) lookups when merging GPS + Accel data.
    
    Args:
        db: SQLAlchemy session
        trip_id: Trip identifier
    
    Returns:
        dict: Timestamp-keyed accelerometer data:
        {
            "2025-01-01T08:00:05Z": {
                "rms_x": 0.12,
                "rms_y": 0.08,
                "rms_z": 0.10,
                "rms_mag": 0.15,
                "max_x": 0.5,
                "max_y": 0.6,
                "max_z": 0.7,
                "max_mag": 0.8,
                "peaks_count": 2,
                "sample_count": 250,
                "flags": 0
            },
            ...
        }
    
    Example:
        >>> accel_map = get_accel_map_for_trip(db, "TRIP_20250101_ESP001_001")
        >>> gps_timestamp = "2025-01-01T08:00:05Z"
        >>> if gps_timestamp in accel_map:
        ...     print(f"RMS magnitude: {accel_map[gps_timestamp]['rms_mag']:.3f}g")
        ... else:
        ...     print("No accel data for this GPS point")
    
    Performance:
        - Uses composite index (DeviceID, Timestamp)
        - Typical time: 5-20ms for 360 points
        - Memory: ~50KB for 360 accel records
    
    Notes:
        - Empty dict if trip has no accelerometer data
        - Timestamps are normalized to match GPS format (UTC ISO with 'Z')
        - Not all GPS points will have accel data (device may skip windows)
    """
    # First, get device_id from trip
    # (We need this because accel is indexed by DeviceID + Timestamp, not trip_id)
    device_id_result = (
        db.query(GPS_data.DeviceID)
        .filter(GPS_data.trip_id == trip_id)
        .limit(1)
        .first()
    )
    
    if not device_id_result:
        # Trip has no GPS data, so no accel either
        return {}
    
    device_id = device_id_result[0]
    
    # Get all timestamps for this trip
    timestamps = (
        db.query(GPS_data.Timestamp)
        .filter(GPS_data.trip_id == trip_id)
        .all()
    )
    
    if not timestamps:
        return {}
    
    # Extract timestamp values
    timestamp_list = [ts[0] for ts in timestamps]
    
    # Query accelerometer data matching these timestamps
    accel_rows = (
        db.query(AccelerometerData)
        .filter(
            AccelerometerData.DeviceID == device_id,
            AccelerometerData.Timestamp.in_(timestamp_list)
        )
        .all()
    )
    
    # Build timestamp-keyed map
    accel_map: dict[str, dict[str, Any]] = {}
    
    for row in accel_rows:
        # Normalize timestamp to match GPS format
        ts = getattr(row, 'Timestamp', None)
        if not ts:
            continue
        
        timestamp_str = ts.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Extract all accelerometer fields
        accel_map[timestamp_str] = {
            "rms_x": float(getattr(row, 'rms_x', 0.0)),
            "rms_y": float(getattr(row, 'rms_y', 0.0)),
            "rms_z": float(getattr(row, 'rms_z', 0.0)),
            "rms_mag": float(getattr(row, 'rms_mag', 0.0)),
            "max_x": float(getattr(row, 'max_x', 0.0)),
            "max_y": float(getattr(row, 'max_y', 0.0)),
            "max_z": float(getattr(row, 'max_z', 0.0)),
            "max_mag": float(getattr(row, 'max_mag', 0.0)),
            "peaks_count": int(getattr(row, 'peaks_count', 0)),
            "sample_count": int(getattr(row, 'sample_count', 0)),
            "flags": int(getattr(row, 'flags', 0))
        }
    
<<<<<<< HEAD
    return accel_map
=======
    return accel_map
>>>>>>> c1e9bfa7c25bd40fab8e243eb393c10b5ddce3d2
