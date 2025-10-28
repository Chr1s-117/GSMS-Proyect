#src/Repositories/gps_data.py

from sqlalchemy.orm import Session
from src.Models.gps_data import GPS_data
from src.Schemas.gps_data import GpsData_create, GpsData_update
from src.Services.gps_serialization import serialize_gps_row, serialize_many
from datetime import datetime


"""
get_gps_data_by_id to get GPS data (from one user) by ID
"""
def get_gps_data_by_id(DB: Session, gps_data_id: int):
    return DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()


# ==========================================================
# ✅ Obtener último GPS por dispositivo (ajustado para geocerca)
# ==========================================================
def get_last_gps_row_by_device(DB: Session, device_id: str, include_id: bool = False) -> dict | None:
    """
    Retrieve the most recent GPS point from a specific device.
    IMPORTANTE: Retorna campos de geocerca SIN serializar para lógica interna.
    """
    row = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.id.desc())
        .first()
    )
    
    if not row:
        print(f"[REPO] get_last_gps_row_by_device('{device_id}'): No GPS anterior encontrado")
        return None

    ts = getattr(row, "Timestamp", None)
    timestamp_iso = ts.isoformat() if ts is not None else None

    result = {
        "id": row.id if include_id else None,
        "DeviceID": row.DeviceID,
        "Latitude": row.Latitude,
        "Longitude": row.Longitude,
        "Altitude": row.Altitude,
        "Accuracy": row.Accuracy,
        "Timestamp": timestamp_iso,
        "CurrentGeofenceID": row.CurrentGeofenceID,
        "CurrentGeofenceName": row.CurrentGeofenceName,
        "GeofenceEventType": row.GeofenceEventType
    }

    print(f"[REPO] get_last_gps_row_by_device('{device_id}'):")
    print(f"[REPO]   → ID en DB: {row.id}")
    print(f"[REPO]   → CurrentGeofenceID: {result['CurrentGeofenceID']}")
    print(f"[REPO]   → GeofenceEventType: {result['GeofenceEventType']}")
    
    return result


# ==========================================================
# ✅ Obtener GPS más antiguo por dispositivo
# ==========================================================
def get_oldest_gps_row_by_device(DB: Session, device_id: str, include_id: bool = False) -> dict | None:
    row = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.id.asc())
        .first()
    )
    return serialize_gps_row(row, include_id=include_id)


# ==========================================================
# ✅ Obtener histórico por dispositivo y rango temporal
# ==========================================================
def get_gps_data_in_range_by_device(
    DB: Session,
    device_id: str,
    start_time: datetime,
    end_time: datetime,
    include_id: bool = False
) -> list[dict]:
    rows = (
        DB.query(GPS_data)
        .filter(
            GPS_data.DeviceID == device_id,
            GPS_data.Timestamp >= start_time,
            GPS_data.Timestamp <= end_time
        )
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=include_id)


# ==========================================================
# ✅ Listar todos los dispositivos que han reportado GPS
# ==========================================================
def get_all_devices(DB: Session) -> list[str]:
    result = DB.query(GPS_data.DeviceID).distinct().all()
    return [row[0] for row in result]


# ==========================================================
# ✅ Obtener última posición de todos los dispositivos
# ==========================================================
def get_last_gps_all_devices(DB: Session, include_id: bool = False) -> dict[str, dict]:
    from sqlalchemy import func, and_
    
    subq = (
        DB.query(
            GPS_data.DeviceID,
            func.max(GPS_data.id).label('max_id')
        )
        .group_by(GPS_data.DeviceID)
        .subquery()
    )
    
    rows = (
        DB.query(GPS_data)
        .join(subq, and_(
            GPS_data.DeviceID == subq.c.DeviceID,
            GPS_data.id == subq.c.max_id
        ))
        .all()
    )
    
    result = {}
    for row in rows:
        serialized = serialize_gps_row(row, include_id=include_id)
        if serialized:
            result[row.DeviceID] = serialized
    
    return result


# ==========================================================
# ✅ Verificar si un dispositivo tiene datos GPS
# ==========================================================
def device_has_gps_data(DB: Session, device_id: str) -> bool:
    count = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .limit(1)
        .count()
    )
    return count > 0


"""
created_gps_data to create a new GPS data row
"""
def created_gps_data(DB: Session, gps_data: GpsData_create):
    new_gps_data = GPS_data(**gps_data.model_dump(exclude_unset=True))
    DB.add(new_gps_data)
    DB.commit()
    DB.refresh(new_gps_data)
    return new_gps_data


"""
update_gps_data to update GPS data row by ID
"""
def update_gps_data(DB: Session, gps_data_id: int, gps_data: GpsData_update):
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if not db_gps_data:
        return None

    update_data = gps_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_gps_data, key, value)

    DB.commit()
    DB.refresh(db_gps_data)
    return db_gps_data


"""
delete_gps_data to delete GPS data row by ID
"""
def delete_gps_data(DB: Session, gps_data_id: int):
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if db_gps_data is None:
        return None
    DB.delete(db_gps_data)
    DB.commit()
    return db_gps_data.id


# ==========================================================
# ⚠️ LEGACY: Histórico global sin filtro de device
# ==========================================================
def get_gps_data_in_range(
    DB: Session, 
    start_time: datetime, 
    end_time: datetime, 
    include_id: bool = False
) -> list[dict]:
    """
    [LEGACY] Retrieve GPS data in time range from ALL devices.
    
    ⚠️ WARNING: Returns mixed GPS data from all devices.
    For device-specific history, use get_gps_data_in_range_by_device().
    
    Use only for:
    - Administrative exports
    - Global monitoring dashboards
    - Debugging
    """
    rows = (
        DB.query(GPS_data)
        .filter(
            GPS_data.Timestamp >= start_time, 
            GPS_data.Timestamp <= end_time
        )
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=include_id)


# ==========================================================
# 📦 FASE 6: Nuevas Funciones en Repository
# ==========================================================
def get_global_oldest_gps(DB: Session) -> dict | None:
    """
    Obtiene el GPS más antiguo de TODOS los devices activos.
    """
    from src.Models.device import Device
    
    row = (
        DB.query(GPS_data)
        .join(Device, GPS_data.DeviceID == Device.DeviceID)
        .filter(Device.IsActive == True)
        .order_by(GPS_data.Timestamp.asc())
        .first()
    )
    return serialize_gps_row(row, include_id=False)


def get_global_newest_gps(DB: Session) -> dict | None:
    """
    Obtiene el GPS más reciente de TODOS los devices activos.
    """
    from src.Models.device import Device
    
    row = (
        DB.query(GPS_data)
        .join(Device, GPS_data.DeviceID == Device.DeviceID)
        .filter(Device.IsActive == True)
        .order_by(GPS_data.Timestamp.desc())
        .first()
    )
    return serialize_gps_row(row, include_id=False)


def get_all_gps_for_device(DB: Session, device_id: str) -> list[dict]:
    """
    Obtiene TODO el historial GPS de un device (sin filtro temporal).
    Úsalo con cuidado en devices con mucha data.
    """
    rows = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=False)
