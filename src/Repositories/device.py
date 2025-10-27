# src/Repositories/device.py

"""
Device Repository Module

This module provides database access functions for Device model operations.

Responsibilities:
- CRUD operations for devices
- Device validation and existence checks
- Device statistics and status management
- Timestamp updates (LastSeen)

Usage:
    from src.Repositories import device as device_repo
    from src.DB.session import SessionLocal
    
    db = SessionLocal()
    all_devices = device_repo.get_all_devices(db)
    
Design Pattern:
    This follows the Repository Pattern to:
    - Separate database logic from business logic
    - Provide reusable query functions
    - Enable easy mocking for tests
    - Ensure consistent transaction handling
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from src.Models.device import Device
from src.Schemas.device import Device_create, Device_update
from typing import List, Optional
from datetime import datetime


# ==========================================================
# 📌 BASIC CRUD OPERATIONS
# ==========================================================

def get_all_devices(db: Session, only_active: bool = False) -> List[Device]:
    """
    Get all devices from the database.
    
    Args:
        db: SQLAlchemy session
        only_active: If True, returns only active devices (default: False)
        
    Returns:
        List of Device objects
        
    Example:
        active_devices = get_all_devices(db, only_active=True)
        all_devices = get_all_devices(db, only_active=False)
    """
    query = db.query(Device)
    
    if only_active:
        query = query.filter(Device.IsActive == True)
    
    return query.all()


def get_device_by_id(db: Session, device_id: str) -> Optional[Device]:
    """
    Get a specific device by its ID.
    
    Args:
        db: SQLAlchemy session
        device_id: Unique identifier of the device
        
    Returns:
        Device object or None if not found
        
    Example:
        device = get_device_by_id(db, "TRUCK-001")
        if device:
            print(f"Device found: {device.Name}")
    """
    return db.query(Device).filter(Device.DeviceID == device_id).first()


def create_device(db: Session, device: Device_create) -> Device:
    """
    Create a new device.
    
    Args:
        db: SQLAlchemy session
        device: Device data (Pydantic schema)
        
    Returns:
        Created Device object
        
    Raises:
        IntegrityError: If device_id already exists (duplicate)
        
    Example:
        new_device = create_device(db, Device_create(
            DeviceID="TRUCK-001",
            Name="Main Truck",
            IsActive=True
        ))
    """
    new_device = Device(**device.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


def update_device(
    db: Session, 
    device_id: str, 
    device: Device_update
) -> Optional[Device]:
    """
    Update an existing device.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device to update
        device: Fields to update (Pydantic schema)
        
    Returns:
        Updated Device object or None if not found
        
    Example:
        updated = update_device(db, "TRUCK-001", Device_update(
            Name="Updated Truck Name",
            IsActive=False
        ))
    """
    db_device = get_device_by_id(db, device_id)
    
    if not db_device:
        return None
    
    # Only update fields that were provided
    update_data = device.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_device, key):
            setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device


def delete_device(db: Session, device_id: str) -> bool:
    """
    Delete a device (hard delete).
    
    ⚠️ WARNING: This permanently removes the device from the database.
    Consider using deactivate_device() for soft delete.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device to delete
        
    Returns:
        True if deleted successfully, False if not found
        
    Example:
        success = delete_device(db, "TRUCK-001")
    """
    db_device = get_device_by_id(db, device_id)
    
    if not db_device:
        return False
    
    db.delete(db_device)
    db.commit()
    return True


def deactivate_device(db: Session, device_id: str) -> bool:
    """
    Deactivate a device (soft delete).
    
    This preserves the device data while marking it as inactive.
    Recommended over hard delete for maintaining historical data integrity.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device to deactivate
        
    Returns:
        True if deactivated successfully, False if not found
        
    Example:
        success = deactivate_device(db, "TRUCK-001")
    """
    db_device = get_device_by_id(db, device_id)
    
    if not db_device:
        return False
    
    db_device.IsActive = False
    db.commit()
    return True


# ==========================================================
# 📌 DEVICE VALIDATION & EXISTENCE CHECKS
# ==========================================================

def device_exists(db: Session, device_id: str) -> bool:
    """
    Check if a device exists in the database.
    
    Args:
        db: SQLAlchemy session
        device_id: ID to check
        
    Returns:
        True if device exists, False otherwise
        
    Example:
        if device_exists(db, "TRUCK-001"):
            print("Device found")
        else:
            raise HTTPException(404, "Device not found")
    """
    return db.query(Device).filter(Device.DeviceID == device_id).count() > 0


def is_device_active(db: Session, device_id: str) -> bool:
    """
    Check if a device is active.
    
    Args:
        db: SQLAlchemy session
        device_id: ID to check
        
    Returns:
        True if device exists and is active, False otherwise
        
    Example:
        if not is_device_active(db, "TRUCK-001"):
            raise HTTPException(403, "Device is inactive")
    """
    device = get_device_by_id(db, device_id)
    return device is not None and device.IsActive


def count_devices(db: Session, only_active: bool = False) -> int:
    """
    Count devices in the database.
    
    Args:
        db: SQLAlchemy session
        only_active: If True, counts only active devices (default: False)
        
    Returns:
        Number of devices
        
    Example:
        total_active = count_devices(db, only_active=True)
        total_all = count_devices(db, only_active=False)
    """
    query = db.query(Device)
    
    if only_active:
        query = query.filter(Device.IsActive == True)
    
    return query.count()


# ==========================================================
# 📌 TIMESTAMP MANAGEMENT
# ==========================================================

def update_last_seen(
    db: Session, 
    device_id: str, 
    timestamp: datetime
) -> bool:
    """
    Update the LastSeen timestamp for a device.
    
    This should be called whenever GPS data is received from the device.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device
        timestamp: UTC timestamp of the GPS data
        
    Returns:
        True if updated successfully, False if device not found
        
    Example:
        # In GPS data insertion logic
        success = update_last_seen(db, "TRUCK-001", gps_data.Timestamp)
    """
    db_device = get_device_by_id(db, device_id)
    
    if not db_device:
        return False
    
    # Only update if the new timestamp is more recent
    if db_device.LastSeen is None or timestamp > db_device.LastSeen:
        db_device.LastSeen = timestamp
        db.commit()
    
    return True


def get_devices_not_seen_since(
    db: Session, 
    threshold: datetime,
    only_active: bool = True
) -> List[Device]:
    """
    Get devices that haven't sent GPS data since a threshold datetime.
    
    Useful for:
    - Finding offline/disconnected devices
    - Health monitoring alerts
    - Automated deactivation of stale devices
    
    Args:
        db: SQLAlchemy session
        threshold: DateTime threshold (e.g., now - 24 hours)
        only_active: If True, only checks active devices (default: True)
        
    Returns:
        List of Device objects not seen since threshold
        
    Example:
        from datetime import datetime, timedelta, timezone
        
        threshold = datetime.now(timezone.utc) - timedelta(hours=24)
        stale_devices = get_devices_not_seen_since(db, threshold)
        
        for device in stale_devices:
            print(f"Device {device.DeviceID} is offline")
    """
    query = db.query(Device).filter(
        (Device.LastSeen < threshold) | (Device.LastSeen == None)
    )
    
    if only_active:
        query = query.filter(Device.IsActive == True)
    
    return query.all()


# ==========================================================
# 📌 DEVICE STATISTICS
# ==========================================================

def get_device_gps_count(db: Session, device_id: str) -> int:
    """
    Get the total number of GPS records from a specific device.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device
        
    Returns:
        Number of GPS records
        
    Example:
        count = get_device_gps_count(db, "TRUCK-001")
        print(f"Device has {count} GPS records")
    """
    from src.Models.gps_data import GPS_data
    
    return db.query(GPS_data).filter(GPS_data.DeviceID == device_id).count()


def get_device_first_gps_timestamp(
    db: Session, 
    device_id: str
) -> Optional[datetime]:
    """
    Get the timestamp of the first GPS record from a device.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device
        
    Returns:
        DateTime of first GPS record or None if no data
        
    Example:
        first_seen = get_device_first_gps_timestamp(db, "TRUCK-001")
        if first_seen:
            print(f"Device first reported: {first_seen}")
    """
    from src.Models.gps_data import GPS_data
    
    result = (
        db.query(func.min(GPS_data.Timestamp))
        .filter(GPS_data.DeviceID == device_id)
        .scalar()
    )
    return result


def get_device_last_gps_timestamp(
    db: Session, 
    device_id: str
) -> Optional[datetime]:
    """
    Get the timestamp of the most recent GPS record from a device.
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device
        
    Returns:
        DateTime of most recent GPS record or None if no data
        
    Example:
        last_seen = get_device_last_gps_timestamp(db, "TRUCK-001")
        if last_seen:
            print(f"Device last reported: {last_seen}")
    """
    from src.Models.gps_data import GPS_data
    
    result = (
        db.query(func.max(GPS_data.Timestamp))
        .filter(GPS_data.DeviceID == device_id)
        .scalar()
    )
    return result


def get_device_current_geofence(db: Session, device_id: str) -> Optional[dict]:
    """
    Get the current geofence of a device (from its latest GPS record).
    
    Args:
        db: SQLAlchemy session
        device_id: ID of the device
        
    Returns:
        Dict with geofence info or None if device has no GPS data
        
    Example:
        geofence_info = get_device_current_geofence(db, "TRUCK-001")
        if geofence_info:
            print(f"Device is in: {geofence_info['name']}")
    """
    from src.Models.gps_data import GPS_data
    
    latest_gps = (
        db.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.id.desc())
        .first()
    )
    
    if not latest_gps or not latest_gps.CurrentGeofenceID:
        return None
    
    return {
        "geofence_id": latest_gps.CurrentGeofenceID,
        "geofence_name": latest_gps.CurrentGeofenceName,
        "event_type": latest_gps.GeofenceEventType,
        "timestamp": latest_gps.Timestamp
    }