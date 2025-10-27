# src/Schemas/geofence.py

"""
Geofence Pydantic Schemas Module

This module defines Pydantic models for geofence data validation
and serialization, with special handling for PostGIS spatial geometries.

Schemas:
- PolygonCoordinates: GeoJSON Polygon structure validation
- GeofenceBase: Common geofence fields with validations
- GeofenceCreate: Schema for creating new geofences
- GeofenceUpdate: Schema for updating geofences (partial updates)
- GeofenceGet: Schema for geofence responses (without geometry)
- GeofenceWithGeometry: Schema for detailed geofence responses
- GeofenceDelete: Schema for deletion confirmations
- GeofenceContainmentCheck: Schema for point-in-polygon queries
- GeofenceListResponse: Schema for paginated geofence lists

GeoJSON Format:
    PostGIS stores geometries in WKT format, but the API accepts/returns GeoJSON.
    Coordinates are in [longitude, latitude] order (NOT lat/lon), following RFC 7946.

Usage:
    from src.Schemas.geofence import GeofenceCreate, GeofenceGet
    
    # Validate incoming GeoJSON
    new_geofence = GeofenceCreate(
        id="warehouse-001",
        name="Main Warehouse",
        geometry={
            "type": "Polygon",
            "coordinates": [[
                [-74.0060, 40.7128],  # lon, lat
                [-74.0050, 40.7128],
                [-74.0050, 40.7120],
                [-74.0060, 40.7120],
                [-74.0060, 40.7128]   # close polygon
            ]]
        }
    )
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


# ============================================================
# GeoJSON Polygon Coordinates Schema
# ============================================================

class PolygonCoordinates(BaseModel):
    """
    GeoJSON Polygon structure for geofence geometry.
    
    PostGIS stores geometries in WKT format, but the API accepts/returns GeoJSON.
    This schema validates the GeoJSON structure before conversion to WKT.
    
    Format:
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [lon1, lat1],  // First point
                    [lon2, lat2],  // Second point
                    [lon3, lat3],  // Third point
                    [lon1, lat1]   // Must close the polygon (same as first point)
                ]
            ]
        }
    
    Note: Coordinates are in [longitude, latitude] order (NOT lat/lon).
          This follows the GeoJSON RFC 7946 standard.
    
    Example:
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [-74.0060, 40.7128],  // New York
                    [-118.2437, 34.0522], // Los Angeles
                    [-87.6298, 41.8781],  // Chicago
                    [-74.0060, 40.7128]   // Close polygon
                ]
            ]
        }
    
    Validation:
        - type must be exactly "Polygon"
        - coordinates must be array of linear rings
        - first and last point of each ring must be identical (closed)
    """
    model_config = ConfigDict(from_attributes=True)

    type: str = Field(
        default="Polygon",
        pattern=r'^Polygon$',
        description="Geometry type (must be 'Polygon')"
    )
    
    coordinates: List[List[List[float]]] = Field(
        ...,
        description="Array of linear rings (outer boundary + optional holes)",
        min_length=1
    )


# ============================================================
# Base Geofence Schema
# ============================================================

class GeofenceBase(BaseModel):
    """
    Base schema for geofences with common attributes and validations.
    
    Defines core geofence properties used across create/update/get operations.
    All geofences must have a name, and can be categorized by type.
    
    Design principles:
    - name is required for identification
    - type allows categorization (warehouse, delivery_zone, etc.)
    - color enables visual distinction on maps
    - is_active allows soft deletion
    - extra_metadata provides extensibility for custom fields
    
    Attributes:
        name: Human-readable geofence name (required, max 200 chars)
        description: Optional detailed description (max 500 chars)
        type: Geofence category (default: 'custom', max 50 chars)
        is_active: Whether geofence is currently active (default: True)
        color: Hex color code for map visualization (default: '#3388ff')
        extra_metadata: Custom JSON data for application-specific fields
    """
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ..., 
        min_length=1, 
        max_length=200,
        description="Human-readable geofence name",
        examples=["Main Warehouse", "Downtown Delivery Zone", "Emergency Response Area"]
    )
    
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional information about the geofence purpose",
        examples=["Primary storage facility", "High-priority delivery area"]
    )
    
    type: str = Field(
        default='custom',
        max_length=50,
        description="Geofence category for filtering and organization",
        examples=["warehouse", "delivery_zone", "restricted_area", "parking", "custom"]
    )
    
    is_active: bool = Field(
        True,
        description="Whether the geofence is currently active for monitoring"
    )
    
    color: str = Field(
        default='#3388ff',
        pattern=r'^#[0-9A-Fa-f]{6}$',
        description="Hex color code for map visualization (e.g., #FF5733)",
        examples=["#3388ff", "#FF5733", "#28a745", "#ffc107"]
    )
    
    extra_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        alias='metadata',
        serialization_alias='metadata',
        description="Custom JSON data for application-specific fields"
    )


# ============================================================
# Create Geofence Schema
# ============================================================

class GeofenceCreate(GeofenceBase):
    """
    Schema for creating a new geofence.
    
    All base fields plus id and geometry are required.
    The id must be unique across all geofences.
    
    Example usage:
        new_geofence = GeofenceCreate(
            id="warehouse-001",
            name="Main Warehouse",
            description="Primary storage facility",
            type="warehouse",
            color="#28a745",
            geometry={
                "type": "Polygon",
                "coordinates": [
                    [
                        [-74.0060, 40.7128],
                        [-74.0050, 40.7128],
                        [-74.0050, 40.7120],
                        [-74.0060, 40.7120],
                        [-74.0060, 40.7128]
                    ]
                ]
            },
            extra_metadata={"capacity": 5000, "manager": "John Doe"}
        )
    
    API endpoint: POST /geofences
    
    Validation:
        - id: Required, 1-100 chars, must be unique
        - geometry: Required, must be valid GeoJSON Polygon
    """
    id: str = Field(
        ..., 
        min_length=1, 
        max_length=100,
        description="Unique geofence identifier (immutable after creation)",
        examples=["warehouse-001", "delivery-zone-downtown", "parking-lot-A"]
    )
    
    geometry: PolygonCoordinates = Field(
        ...,
        description="GeoJSON Polygon defining the geofence boundary"
    )


# ============================================================
# Update Geofence Schema
# ============================================================

class GeofenceUpdate(BaseModel):
    """
    Schema for updating an existing geofence.
    
    All fields are optional to support partial updates via PATCH operations.
    The id cannot be updated (it's the primary key).
    
    Example usage:
        # Update only the color
        update_data = GeofenceUpdate(color="#FF5733")
        
        # Deactivate a geofence
        update_data = GeofenceUpdate(is_active=False)
        
        # Update geometry and metadata
        update_data = GeofenceUpdate(
            geometry={...},
            extra_metadata={"capacity": 6000}
        )
    
    API endpoint: PATCH /geofences/{geofence_id}
    
    Note: Updating geometry will reprocess all current GPS points
          to recalculate geofence containment.
    """
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    type: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    geometry: Optional[PolygonCoordinates] = None
    extra_metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        alias='metadata',
        serialization_alias='metadata'
    )


# ============================================================
# Get Geofence Schema (Response without Geometry)
# ============================================================

class GeofenceGet(GeofenceBase):
    """
    Schema for geofence response data (without geometry).
    
    Used for list endpoints where geometry data would be too large.
    Geometry can be fetched separately via the detail endpoint.
    
    Example response:
        {
            "id": "warehouse-001",
            "name": "Main Warehouse",
            "description": "Primary storage facility",
            "type": "warehouse",
            "is_active": true,
            "color": "#28a745",
            "created_at": "2025-10-22T09:36:08Z",
            "updated_at": "2025-10-22T14:25:33Z",
            "metadata": {"capacity": 5000, "manager": "John Doe"}
        }
    
    API endpoint: GET /geofences (list all)
    """
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(
        ...,
        description="Unique geofence identifier"
    )
    
    created_at: datetime = Field(
        ...,
        description="Timestamp when geofence was created"
    )
    
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp of last modification (null if never updated)"
    )


# ============================================================
# Get Geofence with Geometry Schema
# ============================================================

class GeofenceWithGeometry(GeofenceGet):
    """
    Schema for detailed geofence response (with geometry).
    
    Includes the full GeoJSON geometry for rendering on maps.
    Used when fetching a single geofence by ID.
    
    Example response:
        {
            "id": "warehouse-001",
            "name": "Main Warehouse",
            "description": "Primary storage facility",
            "type": "warehouse",
            "is_active": true,
            "color": "#28a745",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[...]]]
            },
            "created_at": "2025-10-22T09:36:08Z",
            "updated_at": "2025-10-22T14:25:33Z",
            "metadata": {"capacity": 5000, "manager": "John Doe"}
        }
    
    API endpoint: GET /geofences/{geofence_id}
    
    Note: Geometry is converted from PostGIS WKT to GeoJSON in the repository layer.
    """
    geometry: PolygonCoordinates = Field(
        ...,
        description="GeoJSON Polygon geometry of the geofence"
    )


# ============================================================
# Delete Geofence Schema (Response)
# ============================================================

class GeofenceDelete(BaseModel):
    """
    Schema for geofence deletion responses.
    
    Returns confirmation of the deleted geofence ID.
    
    Example response:
        {
            "id": "warehouse-001",
            "status": "deleted"
        }
    
    API endpoint: DELETE /geofences/{geofence_id}
    """
    id: str = Field(
        ...,
        description="ID of the deleted geofence"
    )
    status: str = Field(
        default="deleted",
        description="Operation status"
    )


# ============================================================
# Geofence Containment Check Schema
# ============================================================

class GeofenceContainmentCheck(BaseModel):
    """
    Schema for geofence containment check response.
    
    Used when checking if a GPS point is inside any geofences.
    
    Example response:
        {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "inside_geofences": [
                {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "type": "warehouse",
                    "color": "#28a745"
                }
            ],
            "count": 1
        }
    
    API endpoint: GET /geofences/check/point?latitude=40.7128&longitude=-74.0060
    """
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    inside_geofences: List[GeofenceGet] = Field(
        ...,
        description="List of geofences containing the point"
    )
    count: int = Field(
        ...,
        description="Number of geofences containing the point"
    )


# ============================================================
# Geofence List Response Schema
# ============================================================

class GeofenceListResponse(BaseModel):
    """
    Schema for geofence list with summary statistics.
    
    Example response:
        {
            "geofences": [...],
            "total": 25,
            "active": 22,
            "inactive": 3,
            "by_type": {
                "warehouse": 10,
                "delivery_zone": 8,
                "parking": 4,
                "custom": 3
            }
        }
    
    API endpoint: GET /geofences?include_stats=true
    """
    geofences: List[GeofenceGet] = Field(
        ...,
        description="List of geofence records"
    )
    total: int = Field(
        ...,
        description="Total number of geofences"
    )
    active: int = Field(
        ...,
        description="Number of active geofences"
    )
    inactive: int = Field(
        ...,
        description="Number of inactive geofences"
    )
    by_type: Dict[str, int] = Field(
        ...,
        description="Geofence count grouped by type"
    )