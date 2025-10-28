# src/Repositories/accelerometer_data.py

from sqlalchemy.orm import Session
from src.Models.accelerometer_data import AccelerometerData
from src.Schemas.accelerometer_data import AccelData_create, AccelData_update
from typing import List, Optional
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

