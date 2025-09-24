from pydantic import BaseModel
from typing import Optional
from datetime import datetime


"""
Schema for retrieving GPS data from the database
All fields are required and Timestamp is returned as a datetime object
This ensures ISO 8601 format serialization when sending data to clients

"""

class GpsData_get(BaseModel):
    id: int
    Latitude: float
    Longitude: float
    Altitude: float
    Accuracy: float
    Timestamp: datetime  # UTC-aware datetime, serialized in ISO 8601

    class Config:
        from_attributes = True  # Enables reading attributes directly from ORM models


"""
Schema for creating a new GPS data record
Timestamp must be provided as a datetime object (UTC)}

"""


class GpsData_create(BaseModel):
    Latitude: float
    Longitude: float
    Altitude: float
    Accuracy: float
    Timestamp: datetime  # UTC-aware datetime


"""
Schema for updating an existing GPS data record
All fields are optional to allow partial updates
Timestamp is optional and must be a datetime if provided

"""

class GpsData_update(BaseModel):
    Latitude: Optional[float] = None
    Longitude: Optional[float] = None
    Altitude: Optional[float] = None
    Accuracy: Optional[float] = None
    Timestamp: Optional[datetime] = None  # Optional UTC-aware datetime

"""
Schema for deleting a GPS data record by ID
"""
class GpsData_delete(BaseModel):
    id: int
