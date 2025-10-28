# src/Schemas/accelerometer_data.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class AccelData_base(BaseModel):
    """
    Base schema with common fields for accelerometer data.
    Includes comprehensive validation rules and documentation.
    """
    model_config = ConfigDict(from_attributes=True)

    # Link to GPS data (composite key)
    DeviceID: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Device identifier (must match gps_data.DeviceID)"
    )
    
    Timestamp: datetime = Field(
        ...,
        description="GPS timestamp (must match gps_data.Timestamp, UTC)"
    )

    # Accelerometer window timestamps
    ts_start: datetime = Field(
        ...,
        description="Start of 5-second accelerometer window (UTC)"
    )
    
    ts_end: datetime = Field(
        ...,
        description="End of 5-second accelerometer window (UTC)"
    )

    # RMS values (Root Mean Square) - sustained vibration
    rms_x: float = Field(
        ..., 
        ge=0.0,
        description="RMS acceleration X-axis in g's (≥0)"
    )
    
    rms_y: float = Field(
        ..., 
        ge=0.0,
        description="RMS acceleration Y-axis in g's (≥0)"
    )
    
    rms_z: float = Field(
        ..., 
        ge=0.0,
        description="RMS acceleration Z-axis in g's (≥0)"
    )
    
    rms_mag: float = Field(
        ..., 
        ge=0.0,
        description="RMS vectorial magnitude in g's (≥0)"
    )

    # Maximum absolute values - peak impacts
    max_x: float = Field(
        ..., 
        ge=0.0,
        description="Max absolute acceleration X-axis in g's (≥0)"
    )
    
    max_y: float = Field(
        ..., 
        ge=0.0,
        description="Max absolute acceleration Y-axis in g's (≥0)"
    )
    
    max_z: float = Field(
        ..., 
        ge=0.0,
        description="Max absolute acceleration Z-axis in g's (≥0)"
    )
    
    max_mag: float = Field(
        ..., 
        ge=0.0,
        description="Max vectorial magnitude in g's (≥0)"
    )

    # Statistical counters
    peaks_count: int = Field(
        ..., 
        ge=0,
        description="Number of samples exceeding threshold (≥0)"
    )
    
    sample_count: int = Field(
        ..., 
        ge=1, 
        le=500,
        description="Total samples in window (1-500, expected: 250)"
    )
    
    flags: int = Field(
        default=0,
        ge=0,
        le=255,
        description="Validation flags bitmap (0-255, 0=valid)"
    )


class AccelData_create(AccelData_base):
    """
    Schema for creating new accelerometer data records.
    Used when receiving data from UDP service.
    Inherits all validation rules from base schema.
    """
    pass


class AccelData_update(BaseModel):
    """
    Schema for updating existing accelerometer records.
    All fields are optional to support partial updates.
    Note: Typically accelerometer data is immutable after insertion.
    """
    model_config = ConfigDict(from_attributes=True)

    # Allow partial updates (all optional)
    ts_start: Optional[datetime] = None
    ts_end: Optional[datetime] = None
    
    rms_x: Optional[float] = Field(None, ge=0.0)
    rms_y: Optional[float] = Field(None, ge=0.0)
    rms_z: Optional[float] = Field(None, ge=0.0)
    rms_mag: Optional[float] = Field(None, ge=0.0)
    
    max_x: Optional[float] = Field(None, ge=0.0)
    max_y: Optional[float] = Field(None, ge=0.0)
    max_z: Optional[float] = Field(None, ge=0.0)
    max_mag: Optional[float] = Field(None, ge=0.0)
    
    peaks_count: Optional[int] = Field(None, ge=0)
    sample_count: Optional[int] = Field(None, ge=1, le=500)
    flags: Optional[int] = Field(None, ge=0, le=255)


class AccelData_get(AccelData_base):
    """
    Schema for accelerometer data responses.
    Includes the internal database record ID.
    Used when returning data via HTTP/WebSocket.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Internal database record identifier"
    )