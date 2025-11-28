# src/Schemas/trip.py
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


# ============================================
# BASE SCHEMA
# ============================================
class Trip_base(BaseModel):
    """
    Base schema for Trip with common attributes and validations.
    Used as foundation for Create and Get schemas.
    """
    model_config = ConfigDict(from_attributes=True)
    
    trip_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Unique trip identifier (e.g., TRIP_20250102_ESP001_001)"
    )
    
    device_id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Device that generated this trip"
    )
    
    trip_type: str = Field(
        ...,
        pattern='^(movement|parking)$',
        description="Trip type: 'movement' or 'parking'"
    )
    
    status: str = Field(
        default='active',
        pattern='^(active|closed)$',
        description="Trip status: 'active' or 'closed'"
    )
    
    start_time: datetime = Field(
        ...,
        description="UTC timestamp of trip start"
    )
    
    end_time: Optional[datetime] = Field(
        None,
        description="UTC timestamp of trip end (NULL if active)"
    )
    
    start_lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude of trip start point"
    )
    
    start_lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude of trip start point"
    )


# ============================================
# CREATE SCHEMA
# ============================================
class Trip_create(Trip_base):
    """
    Schema for creating new trips.
    Inherits all base fields with their validations.
    
    Used by:
    - TripDetector when starting new trip
    - Repository create_trip() function
    """
    pass


# ============================================
# UPDATE SCHEMA
# ============================================
class Trip_update(BaseModel):
    """
    Schema for updating existing trips.
    All fields are optional to support partial updates.
    
    Common use cases:
    - Closing trip: update end_time, status='closed', metrics
    - Incrementing point_count
    - Recalculating metrics
    """
    model_config = ConfigDict(from_attributes=True)
    
    status: Optional[str] = Field(
        None,
        pattern='^(active|closed)$'
    )
    
    end_time: Optional[datetime] = None
    
    distance: Optional[float] = Field(
        None,
        ge=0,
        description="Total distance in meters"
    )
    
    duration: Optional[float] = Field(
        None,
        ge=0,
        description="Total duration in seconds"
    )
    
    avg_speed: Optional[float] = Field(
        None,
        ge=0,
        description="Average speed in km/h"
    )
    
    point_count: Optional[int] = Field(
        None,
        ge=0,
        description="Number of GPS points in trip"
    )


# ============================================
# GET SCHEMA
# ============================================
class Trip_get(Trip_base):
    """
    Schema for retrieving trip data from database.
    Includes all base fields plus calculated metrics and audit fields.
    
    Used by:
    - API responses
    - Repository query results
    """
    model_config = ConfigDict(from_attributes=True)
    
    # Calculated metrics (populated when trip closes)
    distance: Optional[float] = Field(
        None,
        description="Total distance traveled in meters"
    )
    
    duration: Optional[float] = Field(
        None,
        description="Total duration in seconds"
    )
    
    avg_speed: Optional[float] = Field(
        None,
        description="Average speed in km/h"
    )
    
    point_count: int = Field(
        default=0,
        description="Number of GPS points in this trip"
    )
    
    # Audit fields
    created_at: datetime = Field(
        ...,
        description="Timestamp when trip record was created"
    )
    
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp of last update"
    )


# ============================================
# SPECIALIZED SCHEMA: Trip Summary
# ============================================
class Trip_summary(BaseModel):
    """
    Lightweight schema for trip lists and summaries.
    Contains only essential fields for performance.
    
    Used by:
    - Dashboard lists
    - Historical reports
    - Quick lookups
    """
    model_config = ConfigDict(from_attributes=True)
    
    trip_id: str
    device_id: str
    trip_type: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    distance: Optional[float] = None
    duration: Optional[float] = None