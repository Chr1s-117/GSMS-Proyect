# src/Repositories/gps_data.py

from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from src.Models.gps_data import GPS_data
from src.Schemas.gps_data import GpsData_create, GpsData_update
from src.Services.gps_serialization import serialize_gps_row, serialize_many
from datetime import datetime
from typing import Optional, List, Dict


# ==========================================================
# 📌 BASIC CRUD OPERATIONS
# ==========================================================

def get_gps_data_by_id(DB: Session, gps_data_id: int):
    """
    Get GPS data record by internal database ID.
    
    Args:
        DB: SQLAlchemy session
        gps_data_id: Internal database ID
        
    Returns:
        GPS_data object or None
    """
    return DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()


def created_gps_data(DB: Session, gps_data: GpsData_create):
    """
    Create a new GPS data row.
    
    Args:
        DB: SQLAlchemy session
        gps_data: GPS data to create (Pydantic schema)
        
    Returns:
        Created GPS_data object
    """
    new_gps_data = GPS_data(**gps_data.model_dump(exclude_unset=True))
    DB.add(new_gps_data)
    DB.commit()
    DB.refresh(new_gps_data)
    return new_gps_data


def update_gps_data(DB: Session, gps_data_id: int, gps_data: GpsData_update):
    """
    Update GPS data row by ID.
    
    Args:
        DB: SQLAlchemy session
        gps_data_id: Internal database ID
        gps_data: Fields to update (Pydantic schema)
        
    Returns:
        Updated GPS_data object or None if not found
    """
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if not db_gps_data:
        return None

    # Only update fields that were sent
    update_data = gps_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_gps_data, key, value)

    DB.commit()
    DB.refresh(db_gps_data)
    return db_gps_data


def delete_gps_data(DB: Session, gps_data_id: int):
    """
    Delete GPS data row by ID.
    
    Args:
        DB: SQLAlchemy session
        gps_data_id: Internal database ID
        
    Returns:
        Deleted record ID or None if not found
    """
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if db_gps_data is None:
        return None
    DB.delete(db_gps_data)
    DB.commit()
    return db_gps_data.id


# ==========================================================
# 📌 DEVICE-SPECIFIC QUERIES (Multi-device support)
# ==========================================================

def get_last_gps_row_by_device(
    DB: Session, 
    device_id: str, 
    include_id: bool = False
) -> Optional[dict]:
    """
    Retrieve the most recent GPS point from a specific device.
    
    IMPORTANT: Returns geofence fields WITHOUT serialization for internal logic.
    Uses idx_device_id_desc index for optimal performance.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        include_id: Whether to include internal DB id in result
        
    Returns:
        Dictionary with GPS data including geofence fields, or None if not found
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

    # Manual serialization to include geofence fields
    ts = getattr(row, "Timestamp", None)
    timestamp_iso = ts.isoformat() if ts is not None else None

    result = {
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
    
    if include_id:
        result["id"] = row.id

    print(f"[REPO] get_last_gps_row_by_device('{device_id}'):")
    print(f"[REPO]   → ID en DB: {row.id}")
    print(f"[REPO]   → CurrentGeofenceID: {result['CurrentGeofenceID']}")
    print(f"[REPO]   → GeofenceEventType: {result['GeofenceEventType']}")
    
    return result


def get_oldest_gps_row_by_device(
    DB: Session, 
    device_id: str, 
    include_id: bool = False
) -> Optional[dict]:
    """
    Retrieve the oldest GPS point from a specific device.
    Uses idx_device_id_asc index for optimal performance.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        include_id: Whether to include internal DB id in result
        
    Returns:
        Dictionary with GPS data or None if not found
    """
    row = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.id.asc())
        .first()
    )
    return serialize_gps_row(row, include_id=include_id)


def get_gps_data_in_range_by_device(
    DB: Session,
    device_id: str,
    start_time: datetime,
    end_time: datetime,
    include_id: bool = False
) -> List[dict]:
    """
    Retrieve GPS data within a time range for a specific device.
    Uses idx_device_timestamp index for optimal performance.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        start_time: Start of time range (inclusive, UTC)
        end_time: End of time range (inclusive, UTC)
        include_id: Whether to include internal DB id in results
        
    Returns:
        List of GPS data dictionaries ordered chronologically
    """
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


def get_all_devices(DB: Session) -> List[str]:
    """
    Get list of all unique DeviceIDs that have reported GPS data.
    
    Args:
        DB: SQLAlchemy session
        
    Returns:
        List of device IDs (e.g., ["TRUCK-001", "TRUCK-002"])
    """
    result = DB.query(GPS_data.DeviceID).distinct().all()
    return [row[0] for row in result]


def get_last_gps_all_devices(DB: Session, include_id: bool = False) -> Dict[str, dict]:
    """
    Get the latest GPS position for ALL devices.
    
    Uses subquery with MAX(id) per device for optimal performance.
    
    Args:
        DB: SQLAlchemy session
        include_id: Whether to include internal DB id in results
        
    Returns:
        Dictionary mapping DeviceID to GPS data:
        {
            "TRUCK-001": {...},
            "TRUCK-002": {...},
            ...
        }
    """
    # Subquery: get max ID per device
    subq = (
        DB.query(
            GPS_data.DeviceID,
            func.max(GPS_data.id).label('max_id')
        )
        .group_by(GPS_data.DeviceID)
        .subquery()
    )
    
    # Main query: get full records for those IDs
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


def device_has_gps_data(DB: Session, device_id: str) -> bool:
    """
    Check if a device has any GPS data in the database.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        
    Returns:
        True if device has at least one GPS record, False otherwise
    """
    count = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .limit(1)
        .count()
    )
    return count > 0


# ==========================================================
# 📌 GLOBAL QUERIES (All devices)
# ==========================================================

def get_gps_data_in_range(
    DB: Session, 
    start_time: datetime, 
    end_time: datetime, 
    include_id: bool = False
) -> List[dict]:
    """
    [LEGACY] Retrieve GPS data in time range from ALL devices.
    
    ⚠️ WARNING: Returns mixed GPS data from all devices.
    For device-specific history, use get_gps_data_in_range_by_device().
    
    Use only for:
    - Administrative exports
    - Global monitoring dashboards
    - Debugging
    
    Args:
        DB: SQLAlchemy session
        start_time: Start of time range (inclusive, UTC)
        end_time: End of time range (inclusive, UTC)
        include_id: Whether to include internal DB id in results
        
    Returns:
        List of GPS data dictionaries ordered chronologically
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


def get_global_oldest_gps(DB: Session) -> Optional[dict]:
    """
    Get the oldest GPS record from ALL active devices.
    
    Joins with Device table to filter only active devices.
    
    Args:
        DB: SQLAlchemy session
        
    Returns:
        Dictionary with GPS data or None if no data exists
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


def get_global_newest_gps(DB: Session) -> Optional[dict]:
    """
    Get the most recent GPS record from ALL active devices.
    
    Joins with Device table to filter only active devices.
    
    Args:
        DB: SQLAlchemy session
        
    Returns:
        Dictionary with GPS data or None if no data exists
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


def get_all_gps_for_device(DB: Session, device_id: str) -> List[dict]:
    """
    Get ALL GPS history for a device (no time filter).
    
    ⚠️ WARNING: Use with caution on devices with large datasets.
    Consider pagination or time-range filtering for production use.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        
    Returns:
        List of GPS data dictionaries ordered chronologically
    """
    rows = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=False)


# ==========================================================
# 📌 GEOFENCE-RELATED QUERIES (FUTURE PHASE)
# ==========================================================

def get_gps_in_geofence(
    DB: Session,
    geofence_id: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None
) -> List[dict]:
    """
    Get all GPS points inside a specific geofence.
    
    Optionally filtered by time range.
    Uses idx_geofence_timestamp index for optimal performance.
    
    Args:
        DB: SQLAlchemy session
        geofence_id: Geofence identifier
        start: Optional start of time range (UTC)
        end: Optional end of time range (UTC)
        
    Returns:
        List of GPS data dictionaries ordered chronologically
    """
    query = DB.query(GPS_data).filter(
        GPS_data.CurrentGeofenceID == geofence_id
    )
    
    if start:
        query = query.filter(GPS_data.Timestamp >= start)
    if end:
        query = query.filter(GPS_data.Timestamp <= end)
    
    rows = query.order_by(GPS_data.Timestamp.asc()).all()
    return serialize_many(rows, include_id=True)


def get_geofence_events_by_device(
    DB: Session,
    device_id: str,
    event_type: Optional[str] = None
) -> List[dict]:
    """
    Get all geofence events (entry/exit/inside) for a device.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        event_type: Optional filter ('entry', 'exit', 'inside')
        
    Returns:
        List of GPS data dictionaries with geofence events, ordered by most recent
    """
    query = DB.query(GPS_data).filter(
        GPS_data.DeviceID == device_id,
        GPS_data.GeofenceEventType.isnot(None)
    )
    
    if event_type:
        query = query.filter(GPS_data.GeofenceEventType == event_type)
    
    rows = query.order_by(GPS_data.Timestamp.desc()).all()
    return serialize_many(rows, include_id=True)