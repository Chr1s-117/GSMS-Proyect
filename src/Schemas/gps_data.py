# src/Schemas/gps_data.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


"""
Base schema with common fields across GPS data models.

Includes field validations and comprehensive documentation.
This schema supports multi-device GPS tracking with geofence integration.

Changes from legacy version:
- Added DeviceID field (required for multi-device support)
- Added geofence-related fields (CurrentGeofenceID, CurrentGeofenceName, GeofenceEventType)
- Added field-level validations (ranges, patterns)
- Uses Pydantic v2 ConfigDict instead of Config class
"""
class GpsData_base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    DeviceID: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="Unique identifier of the GPS device (e.g., 'TRUCK-001')"
    )
    
    Latitude: float = Field(
        ..., 
        ge=-90, 
        le=90, 
        description="Latitude in decimal degrees (WGS84)"
    )
    
    Longitude: float = Field(
        ..., 
        ge=-180, 
        le=180, 
        description="Longitude in decimal degrees (WGS84)"
    )
    
    Altitude: float = Field(
        ..., 
        description="Altitude in meters above sea level"
    )
    
    Accuracy: float = Field(
        ..., 
        ge=0, 
        description="GPS accuracy in meters (horizontal dilution)"
    )
    
    Timestamp: datetime = Field(
        ..., 
        description="UTC timestamp of the GPS reading (ISO 8601 format)"
    )
    
    # Geofence-related fields (optional)
    CurrentGeofenceID: Optional[str] = Field(
        None, 
        max_length=100,
        description="ID of geofence containing this GPS point (null if outside all geofences)"
    )
    
    CurrentGeofenceName: Optional[str] = Field(
        None, 
        max_length=200,
        description="Cached name of current geofence for quick display"
    )
    
    GeofenceEventType: Optional[str] = Field(
        None, 
        pattern=r'^(entry|exit|inside)$',
        description="Geofence event type if this GPS point triggered a transition"
    )


"""
Schema for creating new GPS data records.

All fields from GpsData_base are required except geofence fields.
Timestamp must be provided as a UTC-aware datetime object.

Example usage:
    new_gps = GpsData_create(
        DeviceID="TRUCK-001",
        Latitude=10.9878,
        Longitude=-74.7889,
        Altitude=12.5,
        Accuracy=8.0,
        Timestamp=datetime.now(timezone.utc)
    )
"""
class GpsData_create(GpsData_base):
    pass


"""
Schema for updating existing GPS records.

All fields are optional to support partial updates.
Use this schema for PATCH operations where only specific fields need modification.

Example usage:
    update_data = GpsData_update(
        Accuracy=5.0,
        CurrentGeofenceID="warehouse-001"
    )

Note: Typically GPS data is immutable once created, but this schema
      supports corrections or geofence assignment updates.
"""
class GpsData_update(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    DeviceID: Optional[str] = Field(None, min_length=1, max_length=100)
    Latitude: Optional[float] = Field(None, ge=-90, le=90)
    Longitude: Optional[float] = Field(None, ge=-180, le=180)
    Altitude: Optional[float] = None
    Accuracy: Optional[float] = Field(None, ge=0)
    Timestamp: Optional[datetime] = None
    CurrentGeofenceID: Optional[str] = Field(None, max_length=100)
    CurrentGeofenceName: Optional[str] = Field(None, max_length=200)
    GeofenceEventType: Optional[str] = Field(None, pattern=r'^(entry|exit|inside)$')


"""
Schema for retrieving GPS data from the database.

Includes the internal database record identifier (id) along with all GPS fields.
Timestamp is automatically serialized to ISO 8601 format when returned via API.

This schema is used for:
- GET /gps_data/{id} responses
- WebSocket GPS broadcasts
- Historical GPS data queries

Example response:
    {
        "id": 12345,
        "DeviceID": "TRUCK-001",
        "Latitude": 10.9878,
        "Longitude": -74.7889,
        "Altitude": 12.5,
        "Accuracy": 8.0,
        "Timestamp": "2025-10-22T09:34:28Z",
        "CurrentGeofenceID": "warehouse-001",
        "CurrentGeofenceName": "Main Warehouse",
        "GeofenceEventType": "entry"
    }
"""
class GpsData_get(GpsData_base):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ..., 
        description="Internal database record identifier (auto-generated)"
    )


"""
Schema for GPS data deletion responses.

Returns only the ID of the deleted record as confirmation.

Example usage:
    DELETE /gps_data/12345
    
    Response:
    {
        "id": 12345
    }
"""
class GpsData_delete(BaseModel):
    id: int = Field(
        ..., 
        description="ID of the deleted GPS record"
    )