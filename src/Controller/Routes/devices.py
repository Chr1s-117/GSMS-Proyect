# src/Controller/Routes/devices.py

"""
Device Management REST API

This module provides REST endpoints for managing GPS devices (registration,
activation/deactivation, updates, and statistics).

Endpoints:
- GET    /devices/              List all devices (with filters)
- POST   /devices/              Register new device
- GET    /devices/{device_id}   Get device details
- PATCH  /devices/{device_id}   Update device information
- DELETE /devices/{device_id}   Deactivate device (soft delete)
- GET    /devices/{device_id}/stats  Get device statistics

Security:
- Device registration should be restricted (authentication required in production)
- Only active devices can send GPS data (validated in UDP receiver)
- Deactivation preserves historical GPS data

Integration:
- Used by UDP receiver to validate incoming GPS data
- Used by frontend for device selection dropdowns
- Used by admin panel for device management

Usage:
    # In main.py
    from src.Controller.Routes import devices
    app.include_router(devices.router, prefix="/devices", tags=["devices"])

Created: 2025-10-27
Author: Chr1s-117
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.Controller.deps import get_DB
from src.Repositories import device as device_repo
from src.Schemas import device as device_schema

router = APIRouter()


# ==========================================================
# 📌 List and Filter Devices
# ==========================================================

@router.get("/", response_model=device_schema.Device_list_response)
def list_devices(
    only_active: bool = Query(False, description="Filter only active devices"),
    db: Session = Depends(get_DB)
):
    """
    Get list of all registered devices with optional filtering.
    
    This endpoint returns all devices with statistics and supports
    filtering by active status.
    
    Args:
        only_active: If True, returns only active devices (default: False)
        
    Returns:
        Device list with statistics:
        {
            "devices": [
                {
                    "DeviceID": "TRUCK-001",
                    "Name": "Main Delivery Truck",
                    "Description": "Primary vehicle",
                    "IsActive": true,
                    "CreatedAt": "2025-09-15T08:00:00Z",
                    "LastSeen": "2025-10-27T06:20:00Z"
                },
                ...
            ],
            "total": 25,
            "active": 22,
            "inactive": 3
        }
    
    Example Requests:
        GET /devices/                     # All devices
        GET /devices/?only_active=true    # Only active devices
    
    Use Cases:
        - Admin panel device list
        - Frontend device selector dropdown
        - System health monitoring
        - Device inventory reports
    """
    devices = device_repo.get_all_devices(db, only_active=only_active)
    
    # Calculate statistics
    total = len(devices)
    active = sum(1 for d in devices if d.IsActive)
    inactive = total - active
    
    # Serialize devices using Pydantic schema
    devices_list = [
        device_schema.Device_get.model_validate(device)
        for device in devices
    ]
    
    return {
        "devices": devices_list,
        "total": total,
        "active": active,
        "inactive": inactive
    }


# ==========================================================
# 📌 Get Specific Device
# ==========================================================

@router.get("/{device_id}", response_model=device_schema.Device_get)
def get_device(device_id: str, db: Session = Depends(get_DB)):
    """
    Get details of a specific device.
    
    Returns complete device information including creation timestamp
    and last seen timestamp (last GPS data received).
    
    Args:
        device_id: Unique device identifier (case-sensitive)
        
    Returns:
        Device details:
        {
            "DeviceID": "TRUCK-001",
            "Name": "Main Delivery Truck",
            "Description": "Primary vehicle for downtown routes",
            "IsActive": true,
            "CreatedAt": "2025-09-15T08:00:00Z",
            "LastSeen": "2025-10-27T06:20:00Z"
        }
    
    Example Request:
        GET /devices/TRUCK-001
    
    Raises:
        404: Device not found
    
    Use Cases:
        - Device detail page in admin panel
        - Verify device registration before operations
        - Check device last seen timestamp
    """
    device = device_repo.get_device_by_id(db, device_id)
    
    if device is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Device '{device_id}' not found"
        )
    
    return device


# ==========================================================
# 📌 Register New Device
# ==========================================================

@router.post("/", response_model=device_schema.Device_get, status_code=201)
def register_device(
    device: device_schema.Device_create, 
    db: Session = Depends(get_DB)
):
    """
    Register a new GPS device in the system.
    
    Once registered, the device can send GPS data via UDP receiver.
    If IsActive is set to False, GPS data from this device will be rejected.
    
    Args:
        device: Device data payload
            - DeviceID: Unique identifier (required, 1-100 chars)
            - Name: Human-readable name (optional, max 200 chars)
            - Description: Additional info (optional, max 500 chars)
            - IsActive: Active status (default: True)
        
    Returns:
        Created device with timestamps:
        {
            "DeviceID": "TRUCK-001",
            "Name": "Main Delivery Truck",
            "Description": "Primary vehicle for downtown routes",
            "IsActive": true,
            "CreatedAt": "2025-10-27T06:30:33Z",
            "LastSeen": null
        }
    
    Example Request:
        POST /devices/
        Content-Type: application/json
        
        {
            "DeviceID": "TRUCK-001",
            "Name": "Main Delivery Truck",
            "Description": "Primary vehicle for downtown routes",
            "IsActive": true
        }
    
    Raises:
        409: Device already exists (duplicate DeviceID)
        422: Validation error (invalid field values)
    
    Security Notes:
        - Should require authentication in production
        - Consider IP whitelisting for device registration
        - DeviceID should follow naming convention (e.g., TRUCK-XXX)
    
    Integration:
        - UDP receiver validates DeviceID against this registry
        - Inactive devices are rejected by UDP receiver
        - LastSeen is automatically updated on GPS data receipt
    """
    # Check if device already exists
    if device_repo.device_exists(db, device.DeviceID):
        raise HTTPException(
            status_code=409, 
            detail=f"Device '{device.DeviceID}' already exists"
        )
    
    return device_repo.create_device(db, device)


# ==========================================================
# 📌 Update Device
# ==========================================================

@router.patch("/{device_id}", response_model=device_schema.Device_get)
def update_device(
    device_id: str,
    device: device_schema.Device_update,
    db: Session = Depends(get_DB)
):
    """
    Update device information (name, description, active status).
    
    All fields are optional (partial update supported).
    Use this endpoint to rename devices, update descriptions, or activate/deactivate.
    
    Args:
        device_id: Unique device identifier
        device: Fields to update (all optional)
            - Name: New device name (optional)
            - Description: New description (optional)
            - IsActive: New active status (optional)
        
    Returns:
        Updated device with all fields:
        {
            "DeviceID": "TRUCK-001",
            "Name": "Updated Truck Name",
            "Description": "Updated description",
            "IsActive": false,
            "CreatedAt": "2025-09-15T08:00:00Z",
            "LastSeen": "2025-10-27T06:20:00Z"
        }
    
    Example Requests:
        # Update name only
        PATCH /devices/TRUCK-001
        {"Name": "Updated Truck Name"}
        
        # Deactivate device
        PATCH /devices/TRUCK-001
        {"IsActive": false}
        
        # Update multiple fields
        PATCH /devices/TRUCK-001
        {
            "Name": "New Name",
            "Description": "New Description",
            "IsActive": true
        }
    
    Raises:
        404: Device not found
        422: Validation error (invalid field values)
    
    Use Cases:
        - Rename device after redeployment
        - Update description with current assignment
        - Temporarily deactivate device for maintenance
        - Reactivate device after maintenance
    """
    updated = device_repo.update_device(db, device_id, device)
    
    if updated is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Device '{device_id}' not found"
        )
    
    return updated


# ==========================================================
# 📌 Deactivate Device (Soft Delete)
# ==========================================================

@router.delete("/{device_id}", response_model=device_schema.Device_delete)
def deactivate_device(device_id: str, db: Session = Depends(get_DB)):
    """
    Deactivate a device (soft delete).
    
    This sets IsActive=False, preventing the device from sending GPS data,
    while preserving all historical GPS records for audit and analysis.
    
    Soft delete is preferred over hard delete because:
    - Historical GPS data remains accessible
    - Device can be reactivated if needed
    - Audit trail is preserved
    - No foreign key constraint issues
    
    Args:
        device_id: Unique device identifier
        
    Returns:
        Confirmation message:
        {
            "DeviceID": "TRUCK-001",
            "status": "deactivated"
        }
    
    Example Request:
        DELETE /devices/TRUCK-001
    
    Raises:
        404: Device not found
    
    Behavior After Deactivation:
        - UDP receiver will reject GPS data from this device
        - Device will still appear in device list (with IsActive=false)
        - Historical GPS data remains in database
        - Device can be reactivated with PATCH /devices/{device_id}
    
    Reactivation:
        To reactivate a device, use:
        PATCH /devices/TRUCK-001
        {"IsActive": true}
    
    Use Cases:
        - Device is retired or decommissioned
        - Device is temporarily out of service
        - Device is stolen or lost (prevent unauthorized GPS data)
        - Device is being replaced
    """
    success = device_repo.deactivate_device(db, device_id)
    
    if not success:
        raise HTTPException(
            status_code=404, 
            detail=f"Device '{device_id}' not found"
        )
    
    return {
        "DeviceID": device_id,
        "status": "deactivated"
    }


# ==========================================================
# 📌 Get Device Statistics
# ==========================================================

@router.get("/{device_id}/stats", response_model=device_schema.Device_stats)
def get_device_stats(device_id: str, db: Session = Depends(get_DB)):
    """
    Get operational statistics for a device.
    
    Returns comprehensive metrics about device GPS data and current status.
    Useful for monitoring device health and activity.
    
    Args:
        device_id: Unique device identifier
        
    Returns:
        Device statistics:
        {
            "DeviceID": "TRUCK-001",
            "IsActive": true,
            "TotalGPSPoints": 15342,
            "FirstGPSTimestamp": "2025-09-15T08:00:00Z",
            "LastGPSTimestamp": "2025-10-27T06:20:00Z",
            "CurrentGeofenceID": "warehouse-001",
            "CurrentGeofenceName": "Main Warehouse"
        }
    
    Example Request:
        GET /devices/TRUCK-001/stats
    
    Raises:
        404: Device not found
    
    Statistics Breakdown:
        - TotalGPSPoints: Total number of GPS records from this device
        - FirstGPSTimestamp: When device first reported GPS data
        - LastGPSTimestamp: Most recent GPS data timestamp
        - CurrentGeofenceID: ID of geofence device is currently in (null if outside)
        - CurrentGeofenceName: Name of current geofence (null if outside)
    
    Use Cases:
        - Device health monitoring dashboard
        - Activity reports
        - Billing/usage tracking
        - Troubleshooting connectivity issues
        - Verifying device is reporting data
    """
    device = device_repo.get_device_by_id(db, device_id)
    
    if device is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Device '{device_id}' not found"
        )
    
    # Get GPS statistics from repository
    total_gps = device_repo.get_device_gps_count(db, device_id)
    first_gps = device_repo.get_device_first_gps_timestamp(db, device_id)
    last_gps = device_repo.get_device_last_gps_timestamp(db, device_id)
    current_geofence = device_repo.get_device_current_geofence(db, device_id)
    
    return {
        "DeviceID": device_id,
        "IsActive": device.IsActive,
        "TotalGPSPoints": total_gps,
        "FirstGPSTimestamp": first_gps,
        "LastGPSTimestamp": last_gps,
        "CurrentGeofenceID": current_geofence["geofence_id"] if current_geofence else None,
        "CurrentGeofenceName": current_geofence["geofence_name"] if current_geofence else None
    }