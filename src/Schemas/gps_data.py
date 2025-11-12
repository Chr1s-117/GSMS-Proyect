# src/Schemas/gps_data.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


"""
Base schema with common fields across GPS data models.
Includes field validations and comprehensive documentation.
"""
class GpsData_base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    DeviceID: str = Field(..., min_length=1, max_length=100, description="ID of the device that sent the GPS point")
    
    # ========================================
    # NUEVO: Trip relationship
    # ========================================
    trip_id: Optional[str] = Field(
        None, 
        max_length=100,
        description="ID of the trip this GPS belongs to (NULL for legacy data)"
    )

    Latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    Longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    Altitude: float = Field(..., description="Altitude in meters above sea level")
    Accuracy: float = Field(..., ge=0, description="GPS point accuracy in meters")
    Timestamp: datetime = Field(..., description="UTC timestamp of the GPS point")
    CurrentGeofenceID: Optional[str] = Field(None, max_length=100)
    CurrentGeofenceName: Optional[str] = Field(None, max_length=200)
    GeofenceEventType: Optional[str] = Field(None, pattern='^(entry|exit|inside)$')


"""
Schema for creating new GPS data records.
Inherits all fields from the base schema with required validations.
<<<<<<< HEAD
"""
class GpsData_create(GpsData_base):
    pass


"""
Schema for updating existing GPS records.
All fields are optional to support partial updates.
"""
class GpsData_update(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    DeviceID: Optional[str] = Field(None, min_length=1, max_length=100)
    
    # ========================================
    # NUEVO: Trip relationship
    # ========================================
    trip_id: Optional[str] = Field(None, max_length=100)
    
    Latitude: Optional[float] = Field(None, ge=-90, le=90)
    Longitude: Optional[float] = Field(None, ge=-180, le=180)
    Altitude: Optional[float] = None
    Accuracy: Optional[float] = Field(None, ge=0)
    Timestamp: Optional[datetime] = None


"""
=======
"""
class GpsData_create(GpsData_base):
    pass

"""
Schema for updating existing GPS records.
All fields are optional to support partial updates.
"""
class GpsData_update(BaseModel):
    model_config = ConfigDict(from_attributes=True)

"""
Schema for updating existing GPS records.
All fields are optional to support partial updates.
"""
class GpsData_update(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    DeviceID: Optional[str] = Field(None, min_length=1, max_length=100)
    
    # ========================================
    # NUEVO: Trip relationship
    # ========================================
    trip_id: Optional[str] = Field(None, max_length=100)
    
    Latitude: Optional[float] = Field(None, ge=-90, le=90)
    Longitude: Optional[float] = Field(None, ge=-180, le=180)
    Altitude: Optional[float] = None
    Accuracy: Optional[float] = Field(None, ge=0)
    Timestamp: Optional[datetime] = None


"""
Schema for retrieving GPS data from the database.
Includes the internal record identifier.
"""
class GpsData_get(GpsData_base):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Internal database record identifier")


"""
Schema for deleting GPS records by their unique identifier.
"""
class GpsData_delete(BaseModel):
    id: int
