# src/Schemas/device.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


"""
Base schema for GPS devices with common attributes and validations.

Defines the core device properties used across the application.
This schema supports device registration, tracking, and management
in a multi-device GPS tracking system.

Design principles:
- DeviceID is immutable after creation (not in update schema)
- Name and Description are optional for flexibility
- IsActive defaults to True for new devices
"""
class Device_base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    DeviceID: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Unique device identifier (e.g., 'TRUCK-001', 'FLEET-ALPHA-05')",
        examples=["TRUCK-001", "VEHICLE-123", "GPS-TRACKER-A1"]
    )
    
    Name: Optional[str] = Field(
        None, 
        max_length=200, 
        description="Human-readable device name for display purposes",
        examples=["Main Delivery Truck", "North Route Vehicle", "Emergency Response Unit"]
    )
    
    Description: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Additional device information (model, driver, route, etc.)",
        examples=["2024 Ford F-150, Driver: John Doe", "Primary delivery vehicle for Zone A"]
    )
    
    IsActive: bool = Field(
        True, 
        description="Device operational status (active devices can send GPS data)"
    )


"""
Schema for registering new GPS devices.

All fields from Device_base are inherited with required validations.
DeviceID must be unique across all devices in the system.

Example usage:
    new_device = Device_create(
        DeviceID="TRUCK-001",
        Name="Main Delivery Truck",
        Description="Primary vehicle for downtown routes",
        IsActive=True
    )

API endpoint: POST /devices
"""
class Device_create(Device_base):
    pass


"""
Schema for updating existing device records.

All fields are optional to support partial updates via PATCH operations.
DeviceID cannot be updated (it's the primary key).

Example usage:
    # Update only the name
    update_data = Device_update(Name="Updated Truck Name")
    
    # Deactivate a device
    update_data = Device_update(IsActive=False)
    
    # Update multiple fields
    update_data = Device_update(
        Name="New Name",
        Description="New Description",
        IsActive=False
    )

API endpoint: PATCH /devices/{device_id}

Note: For device deactivation, prefer using dedicated endpoint
      DELETE /devices/{device_id} for better semantics.
"""
class Device_update(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    Name: Optional[str] = Field(None, max_length=200)
    Description: Optional[str] = Field(None, max_length=500)
    IsActive: Optional[bool] = None


"""
Schema for device response data including system timestamps.

Used when retrieving device information from the database.
Includes all base fields plus auto-generated timestamps.

Example response:
    {
        "DeviceID": "TRUCK-001",
        "Name": "Main Delivery Truck",
        "Description": "Primary vehicle for downtown routes",
        "IsActive": true,
        "CreatedAt": "2025-10-22T09:36:08Z",
        "LastSeen": "2025-10-22T14:25:33Z"
    }

API endpoints:
- GET /devices (list all devices)
- GET /devices/{device_id} (get specific device)

Fields:
- CreatedAt: Timestamp when device was first registered
- LastSeen: Timestamp of last GPS data received (null if never sent data)
"""
class Device_get(Device_base):
    model_config = ConfigDict(from_attributes=True)

    CreatedAt: datetime = Field(
        ..., 
        description="Timestamp when the device was registered in the system"
    )
    
    LastSeen: Optional[datetime] = Field(
        None, 
        description="Timestamp of last GPS data received from this device (null if no data yet)"
    )


"""
Schema for device deletion responses.

Returns confirmation of the deleted device ID.

Example response:
    {
        "DeviceID": "TRUCK-001",
        "status": "deactivated"
    }

API endpoint: DELETE /devices/{device_id}
"""
class Device_delete(BaseModel):
    DeviceID: str = Field(
        ..., 
        description="ID of the deleted/deactivated device"
    )
    status: str = Field(
        default="deactivated",
        description="Operation status"
    )


"""
Schema for device list with summary statistics.

Used for endpoints that return multiple devices with metadata.

Example response:
    {
        "devices": [
            {
                "DeviceID": "TRUCK-001",
                "Name": "Main Truck",
                "IsActive": true,
                "CreatedAt": "2025-10-22T09:36:08Z",
                "LastSeen": "2025-10-22T14:25:33Z"
            },
            ...
        ],
        "total": 15,
        "active": 12,
        "inactive": 3
    }
"""
class Device_list_response(BaseModel):
    devices: list[Device_get] = Field(
        ..., 
        description="List of device records"
    )
    total: int = Field(
        ..., 
        description="Total number of devices"
    )
    active: int = Field(
        ..., 
        description="Number of active devices"
    )
    inactive: int = Field(
        ..., 
        description="Number of inactive devices"
    )


"""
Schema for device statistics and health monitoring.

Provides operational metrics for a specific device.

Example response:
    {
        "DeviceID": "TRUCK-001",
        "IsActive": true,
        "TotalGPSPoints": 15342,
        "FirstGPSTimestamp": "2025-09-15T08:00:00Z",
        "LastGPSTimestamp": "2025-10-22T14:25:33Z",
        "CurrentGeofenceID": "warehouse-001",
        "CurrentGeofenceName": "Main Warehouse"
    }

API endpoint: GET /devices/{device_id}/stats
"""
class Device_stats(BaseModel):
    DeviceID: str
    IsActive: bool
    TotalGPSPoints: int = Field(
        ..., 
        description="Total number of GPS records from this device"
    )
    FirstGPSTimestamp: Optional[datetime] = Field(
        None, 
        description="Timestamp of first GPS data (null if no data)"
    )
    LastGPSTimestamp: Optional[datetime] = Field(
        None, 
        description="Timestamp of most recent GPS data (null if no data)"
    )
    CurrentGeofenceID: Optional[str] = Field(
        None, 
        description="ID of current geofence (null if outside all geofences)"
    )
    CurrentGeofenceName: Optional[str] = Field(
        None, 
        description="Name of current geofence (null if outside)"
    )