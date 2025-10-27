# src/Schemas/gps_data.py

"""
GPS Data Pydantic Schemas Module

This module defines Pydantic models for GPS tracking data validation
and serialization, with support for geofence association.

Schemas:
- GpsData_base: Common GPS fields with validations
- GpsData_create: Schema for inserting new GPS records
- GpsData_update: Schema for updating GPS records (partial updates)
- GpsData_get: Schema for GPS data responses with internal ID
- GpsData_delete: Schema for deletion by ID

New Features (v2.0):
    - DeviceID field for multi-device tracking
    - Geofence association fields (CurrentGeofenceID, CurrentGeofenceName)
    - GeofenceEventType for entry/exit/inside events

Usage:
    from src.Schemas.gps_data import GpsData_create, GpsData_get
    
    # Validate incoming GPS data
    new_gps = GpsData_create(
        DeviceID="TRUCK-001",
        Latitude=40.7128,
        Longitude=-74.0060,
        Altitude=10.5,
        Accuracy=5.0,
        Timestamp=datetime.now(timezone.utc),
        CurrentGeofenceID="warehouse-001",
        GeofenceEventType="entry"
    )
    
    # Serialize database model to response
    gps_response = GpsData_get.model_validate(db_gps_record)
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


# ============================================================
# Base GPS Data Schema
# ============================================================

class GpsData_base(BaseModel):
    """
    Base schema with common fields across GPS data models.
    
    Includes field validations and comprehensive documentation.
    All GPS coordinates are validated against geographic bounds.
    
    Attributes:
        DeviceID: Unique identifier of the device that sent this GPS point
        Latitude: Latitude in decimal degrees (-90 to +90)
        Longitude: Longitude in decimal degrees (-180 to +180)
        Altitude: Altitude in meters above sea level
        Accuracy: GPS point accuracy/precision in meters (≥ 0)
        Timestamp: UTC timestamp when GPS reading was recorded
        CurrentGeofenceID: ID of geofence containing this point (null if outside)
        CurrentGeofenceName: Cached geofence name for quick display
        GeofenceEventType: Event type (entry/exit/inside) if transition occurred
    """
    model_config = ConfigDict(from_attributes=True)

    DeviceID: str = Field(
        ..., 
        min_length=1, 
        max_length=100, 
        description="ID of the device that sent the GPS point"
    )
    
    Latitude: float = Field(
        ..., 
        ge=-90, 
        le=90, 
        description="Latitude in decimal degrees (range: -90 to +90)"
    )
    
    Longitude: float = Field(
        ..., 
        ge=-180, 
        le=180, 
        description="Longitude in decimal degrees (range: -180 to +180)"
    )
    
    Altitude: float = Field(
        ..., 
        description="Altitude in meters above sea level"
    )
    
    Accuracy: float = Field(
        ..., 
        ge=0, 
        description="GPS point accuracy/precision in meters (lower is better)"
    )
    
    Timestamp: datetime = Field(
        ..., 
        description="UTC timestamp of the GPS point (timezone-aware)"
    )
    
    CurrentGeofenceID: Optional[str] = Field(
        None, 
        max_length=100,
        description="ID of geofence containing this GPS point (null if outside all geofences)"
    )
    
    CurrentGeofenceName: Optional[str] = Field(
        None, 
        max_length=200,
        description="Cached geofence name for quick display without JOIN"
    )
    
    GeofenceEventType: Optional[str] = Field(
        None, 
        pattern='^(entry|exit|inside)$',
        description="Event type if this GPS point triggered a geofence transition: entry, exit, inside"
    )


# ============================================================
# Create GPS Data Schema
# ============================================================

class GpsData_create(GpsData_base):
    """
    Schema for creating new GPS data records.
    
    Inherits all fields from the base schema with required validations.
    Timestamp must be provided as a timezone-aware datetime (UTC).
    
    Example usage:
        from datetime import datetime, timezone
        
        new_gps = GpsData_create(
            DeviceID="TRUCK-001",
            Latitude=40.7128,
            Longitude=-74.0060,
            Altitude=10.5,
            Accuracy=5.0,
            Timestamp=datetime.now(timezone.utc),
            CurrentGeofenceID="warehouse-001",
            CurrentGeofenceName="Main Warehouse",
            GeofenceEventType="entry"
        )
    
    API endpoint: POST /gps_data
    
    Validation:
        - All fields from GpsData_base are required
        - Timestamp must be timezone-aware (UTC)
        - Latitude: -90 to +90
        - Longitude: -180 to +180
        - Accuracy: ≥ 0
        - GeofenceEventType: 'entry', 'exit', or 'inside' (if provided)
    """
    pass


# ============================================================
# Update GPS Data Schema
# ============================================================

class GpsData_update(BaseModel):
    """
    Schema for updating existing GPS records.
    
    All fields are optional to support partial updates via PATCH operations.
    The internal record ID cannot be updated (it's the primary key).
    
    Example usage:
        # Update geofence association
        update_data = GpsData_update(
            CurrentGeofenceID="warehouse-002",
            CurrentGeofenceName="North Warehouse",
            GeofenceEventType="entry"
        )
        
        # Correct GPS coordinates
        update_data = GpsData_update(
            Latitude=40.7130,
            Longitude=-74.0062
        )
    
    API endpoint: PATCH /gps_data/{gps_id}
    
    Note: Updating GPS coordinates is generally not recommended.
          GPS records should be immutable for audit purposes.
    """
    model_config = ConfigDict(from_attributes=True)

    DeviceID: Optional[str] = Field(None, min_length=1, max_length=100)
    Latitude: Optional[float] = Field(None, ge=-90, le=90)
    Longitude: Optional[float] = Field(None, ge=-180, le=180)
    Altitude: Optional[float] = None
    Accuracy: Optional[float] = Field(None, ge=0)
    Timestamp: Optional[datetime] = None


# ============================================================
# Get GPS Data Schema (Response)
# ============================================================

class GpsData_get(GpsData_base):
    """
    Schema for retrieving GPS data from the database.
    
    Includes all base fields plus the internal database record identifier.
    Timestamp is serialized in ISO 8601 format for API responses.
    
    Example response:
        {
            "id": 12345,
            "DeviceID": "TRUCK-001",
            "Latitude": 40.7128,
            "Longitude": -74.0060,
            "Altitude": 10.5,
            "Accuracy": 5.0,
            "Timestamp": "2025-10-22T14:25:33Z",
            "CurrentGeofenceID": "warehouse-001",
            "CurrentGeofenceName": "Main Warehouse",
            "GeofenceEventType": "entry"
        }
    
    API endpoints:
        - GET /gps_data (list all GPS records)
        - GET /gps_data/{gps_id} (get specific GPS record)
        - GET /gps_data/device/{device_id} (get GPS records for a device)
    
    Fields:
        id: Internal database record identifier (auto-generated)
        All other fields from GpsData_base
    """
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ..., 
        description="Internal database record identifier (auto-generated)"
    )


# ============================================================
# Delete GPS Data Schema
# ============================================================

class GpsData_delete(BaseModel):
    """
    Schema for deleting GPS records by their unique identifier.
    
    Example request:
        DELETE /gps_data/12345
    
    Example response:
        {
            "id": 12345,
            "status": "deleted"
        }
    
    API endpoint: DELETE /gps_data/{gps_id}
    
    Note: Deleting GPS records is generally not recommended.
          Consider soft deletion or archiving instead for audit purposes.
    """
    id: int = Field(
        ...,
        description="Internal database record identifier of the GPS record to delete"
    )