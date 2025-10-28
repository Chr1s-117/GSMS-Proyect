# src/Schemas/device.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class Device_base(BaseModel):
    """
    Base schema for GPS devices with common attributes and validations.
    Defines the core device properties used across the application.
    """
    model_config = ConfigDict(from_attributes=True)

    DeviceID: str = Field(..., min_length=1, max_length=100, description="Unique device identifier")
    Name: Optional[str] = Field(None, max_length=200, description="Descriptive name (e.g., 'Truck 01')")
    Description: Optional[str] = Field(None, max_length=500, description="Additional device description")
    IsActive: bool = Field(True, description="Device active status")


class Device_create(Device_base):
    """
    Schema for registering new GPS devices.
    Inherits all base fields with required validations.
    """
    pass


class Device_update(BaseModel):
    """
    Schema for updating existing device records.
    All fields are optional to support partial updates.
    """
    model_config = ConfigDict(from_attributes=True)

    Name: Optional[str] = Field(None, max_length=200)
    Description: Optional[str] = Field(None, max_length=500)
    IsActive: Optional[bool] = None


class Device_get(Device_base):
    """
    Schema for device response data including system timestamps.
    Used when retrieving device information from the database.
    """
    model_config = ConfigDict(from_attributes=True)

    CreatedAt: datetime
    LastSeen: Optional[datetime] = None