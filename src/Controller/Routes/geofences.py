# src/Controller/Routes/geofences.py

"""
Geofence Management REST API

This module provides REST endpoints for managing geofences (geographic boundaries)
with PostGIS spatial operations for real-time geofence detection.

Endpoints:
- GET    /geofences/                     List all geofences (with filters)
- POST   /geofences/                     Create new geofence
- GET    /geofences/{geofence_id}        Get geofence details with geometry
- PATCH  /geofences/{geofence_id}        Update geofence
- DELETE /geofences/{geofence_id}        Delete/deactivate geofence
- GET    /geofences/check/point          Check if point is inside any geofence
- POST   /geofences/import               Bulk import from GeoJSON file

PostGIS Requirements:
- PostgreSQL with PostGIS extension enabled (CREATE EXTENSION postgis;)
- SRID 4326 (WGS84) coordinate system for GPS compatibility
- Spatial index on geometry column (GIST) for fast queries

GeoJSON Format:
- Coordinates are in [longitude, latitude] order (NOT lat/lon)
- Polygon must be closed (first point = last point)
- Follows RFC 7946 standard

Integration:
- Used by UDP receiver to detect geofence entry/exit events
- Used by frontend for geofence visualization and management
- Used by reporting system for location-based analytics

Usage:
    # In main.py
    from src.Controller.Routes import geofences
    app.include_router(geofences.router, prefix="/geofences", tags=["geofences"])

Created: 2025-10-27
Author: Chr1s-117
"""

# Standard library
import tempfile
import os
from typing import Optional, List

# FastAPI
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session

# Internal dependencies
from src.Controller.deps import get_DB
from src.Repositories import geofence as geofence_repo
from src.Schemas import geofence as geofence_schema
from src.Services.geofence_importer import GeofenceImporter

# GeoAlchemy2 and Shapely (for PostGIS geometry handling)
from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKTElement
from shapely.geometry import shape, mapping

router = APIRouter()


# ==========================================================
# 📌 List and Filter Geofences
# ==========================================================

@router.get("/", response_model=geofence_schema.GeofenceListResponse)
def list_geofences(
    only_active: bool = Query(True, description="Filter only active geofences"),
    type: Optional[str] = Query(None, description="Filter by geofence type"),
    db: Session = Depends(get_DB)
):
    """
    Get list of all geofences with optional filtering and statistics.
    
    Returns geofences WITHOUT geometry for performance.
    Use GET /geofences/{id} to get geometry for specific geofence.
    
    Args:
        only_active: If True, returns only active geofences (default: True)
        type: Optional filter by geofence type (e.g., "warehouse", "delivery_zone")
        
    Returns:
        Geofence list with statistics:
        {
            "geofences": [
                {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "description": "Primary storage facility",
                    "type": "warehouse",
                    "is_active": true,
                    "color": "#28a745",
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": "2025-10-01T12:00:00Z",
                    "metadata": {"capacity": 5000}
                },
                ...
            ],
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
    
    Example Requests:
        GET /geofences/                          # All active geofences
        GET /geofences/?only_active=false        # All geofences (including inactive)
        GET /geofences/?type=warehouse           # Only warehouses
        GET /geofences/?type=delivery_zone&only_active=true
    
    Performance Note:
        Geometry is NOT included in list response to reduce payload size.
        For large geofences, geometry can be several KB per record.
        Use GET /geofences/{id} to get geometry when needed.
    
    Use Cases:
        - Admin panel geofence list
        - Frontend geofence selector
        - Statistics dashboard
        - Type-based filtering
    """
    if type:
        geofences = geofence_repo.get_geofences_by_type(db, type, only_active=only_active)
    else:
        geofences = geofence_repo.get_all_geofences(db, only_active=only_active)
    
    # Calculate statistics
    total = len(geofences)
    active = sum(1 for g in geofences if g.is_active)
    inactive = total - active
    
    # Group by type
    by_type = {}
    for g in geofences:
        by_type[g.type] = by_type.get(g.type, 0) + 1
    
    geofences_list = [
        geofence_schema.GeofenceGet.model_validate(geofence, from_attributes=True)
        for geofence in geofences
    ]
    
    return {
        "geofences": geofences_list,
        "total": total,
        "active": active,
        "inactive": inactive,
        "by_type": by_type
    }


# ==========================================================
# 📌 Get Specific Geofence (with Geometry)
# ==========================================================

@router.get("/{geofence_id}", response_model=geofence_schema.GeofenceWithGeometry)
def get_geofence(geofence_id: str, db: Session = Depends(get_DB)):
    """
    Get details of a specific geofence including GeoJSON geometry.
    
    Returns complete geofence data with geometry for map rendering.
    Geometry is converted from PostGIS internal format to GeoJSON.
    
    Args:
        geofence_id: Unique geofence identifier (case-sensitive)
        
    Returns:
        Geofence details with GeoJSON geometry:
        {
            "id": "warehouse-001",
            "name": "Main Warehouse",
            "description": "Primary storage facility",
            "type": "warehouse",
            "is_active": true,
            "color": "#28a745",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-74.0060, 40.7128],  // [longitude, latitude]
                        [-74.0050, 40.7128],
                        [-74.0050, 40.7120],
                        [-74.0060, 40.7120],
                        [-74.0060, 40.7128]   // closed polygon
                    ]
                ]
            },
            "created_at": "2025-09-01T00:00:00Z",
            "updated_at": "2025-10-01T12:00:00Z",
            "metadata": {"capacity": 5000}
        }
    
    Example Request:
        GET /geofences/warehouse-001
    
    Raises:
        404: Geofence not found
    
    GeoJSON Format:
        - Coordinates are [longitude, latitude] (NOT lat, lon)
        - Follows RFC 7946 standard
        - Compatible with Leaflet, Mapbox, Google Maps
    
    Use Cases:
        - Display geofence boundary on map
        - Edit geofence in map editor
        - Export geofence for external use
        - Validate geofence geometry
    """
    geofence = geofence_repo.get_geofence_by_id(db, geofence_id)
    
    if geofence is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Geofence '{geofence_id}' not found"
        )
    
    # Convert PostGIS geometry to GeoJSON
    
    try:
        shapely_geom = to_shape(geofence.geometry)
        geojson_geom = mapping(shapely_geom)
        
        # Serialize to Pydantic schema
        geofence_dict = geofence_schema.GeofenceGet.model_validate(geofence, from_attributes=True).model_dump()
        geofence_dict["geometry"] = geojson_geom
        
        return geofence_dict
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error converting geometry to GeoJSON: {str(e)}"
        )


# ==========================================================
# 📌 Create Geofence
# ==========================================================

@router.post("/", response_model=geofence_schema.GeofenceGet, status_code=201)
def create_geofence(
    geofence: geofence_schema.GeofenceCreate,
    db: Session = Depends(get_DB)
):
    """
    Create a new geofence with GeoJSON geometry.
    
    Geometry is converted from GeoJSON to PostGIS internal format (WKT)
    and stored with SRID 4326 (WGS84) for GPS compatibility.
    
    Args:
        geofence: Geofence data payload
            - id: Unique identifier (required, 1-100 chars)
            - name: Human-readable name (required, max 200 chars)
            - description: Additional info (optional, max 500 chars)
            - type: Geofence category (default: "custom", max 50 chars)
            - is_active: Active status (default: True)
            - color: Hex color for map (default: "#3388ff", must match #RRGGBB)
            - geometry: GeoJSON Polygon (required)
            - metadata: Custom JSON data (optional)
        
    Returns:
        Created geofence (without geometry in response):
        {
            "id": "warehouse-001",
            "name": "Main Warehouse",
            "description": "Primary storage facility",
            "type": "warehouse",
            "is_active": true,
            "color": "#28a745",
            "created_at": "2025-10-27T06:30:33Z",
            "updated_at": null,
            "metadata": {"capacity": 5000}
        }
    
    Example Request:
        POST /geofences/
        Content-Type: application/json
        
        {
            "id": "warehouse-001",
            "name": "Main Warehouse",
            "description": "Primary storage facility",
            "type": "warehouse",
            "is_active": true,
            "color": "#28a745",
            "geometry": {
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
            "metadata": {"capacity": 5000, "manager": "John Doe"}
        }
    
    Raises:
        409: Geofence with this ID already exists
        422: Invalid geometry or validation error
    
    Geometry Validation:
        - Must be valid GeoJSON Polygon
        - Polygon must be closed (first point = last point)
        - Coordinates in [longitude, latitude] order
        - No self-intersections
        - Minimum 3 unique points (4 including closure)
    
    Integration:
        - UDP receiver uses this geofence for real-time detection
        - Spatial index (GIST) is automatically used for fast queries
        - Geometry is stored in Geography type (spherical calculations)
    """
    # Check if geofence already exists
    if geofence_repo.geofence_exists(db, geofence.id):
        raise HTTPException(
            status_code=409, 
            detail=f"Geofence '{geofence.id}' already exists"
        )
    
    # Convert GeoJSON to PostGIS WKT
    
    try:
        # Validate and convert GeoJSON to Shapely geometry
        geojson_dict = geofence.geometry.model_dump()
        shapely_geom = shape(geojson_dict)
        
        # Validate geometry
        if not shapely_geom.is_valid:
            raise ValueError("Geometry is not valid (self-intersections or other issues)")
        
        # Convert to WKT with SRID 4326
        wkt_geom = WKTElement(shapely_geom.wkt, srid=4326)
        
        # Create geofence using repository
        created = geofence_repo.create_geofence(db, geofence)
        
        return created
        
    except ValueError as ve:
        raise HTTPException(
            status_code=422, 
            detail=f"Invalid geometry: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=422, 
            detail=f"Error processing geometry: {str(e)}"
        )


# ==========================================================
# 📌 Update Geofence
# ==========================================================

@router.patch("/{geofence_id}", response_model=geofence_schema.GeofenceGet)
def update_geofence(
    geofence_id: str,
    geofence: geofence_schema.GeofenceUpdate,
    db: Session = Depends(get_DB)
):
    """
    Update geofence information (partial update supported).
    
    All fields are optional. Only provided fields will be updated.
    Geometry can be updated, triggering re-detection for all current GPS points.
    
    Args:
        geofence_id: Unique geofence identifier
        geofence: Fields to update (all optional)
            - name: New name (optional)
            - description: New description (optional)
            - type: New type (optional)
            - is_active: New active status (optional)
            - color: New color (optional, must match #RRGGBB)
            - geometry: New GeoJSON geometry (optional)
            - metadata: New metadata (optional)
        
    Returns:
        Updated geofence (without geometry):
        {
            "id": "warehouse-001",
            "name": "Updated Warehouse Name",
            ...
        }
    
    Example Requests:
        # Update name only
        PATCH /geofences/warehouse-001
        {"name": "Updated Warehouse Name"}
        
        # Deactivate geofence
        PATCH /geofences/warehouse-001
        {"is_active": false}
        
        # Update geometry (re-detection triggered)
        PATCH /geofences/warehouse-001
        {
            "geometry": {
                "type": "Polygon",
                "coordinates": [[...]]
            }
        }
    
    Raises:
        404: Geofence not found
        422: Invalid geometry or validation error
    
    Warning:
        Updating geometry will affect future geofence detections.
        Historical GPS records are NOT retroactively updated.
        Consider creating a new geofence if boundary significantly changes.
    """
    # Convert GeoJSON geometry to WKT if provided
    if geofence.geometry:
        
        try:
            geojson_dict = geofence.geometry.model_dump()
            shapely_geom = shape(geojson_dict)
            
            if not shapely_geom.is_valid:
                raise ValueError("Geometry is not valid")
            
            wkt_geom = WKTElement(shapely_geom.wkt, srid=4326)
            
            # Create update dict with WKT geometry
            geofence_dict = geofence.model_dump(exclude_unset=True)
            geofence_dict["geometry"] = wkt_geom
            
        except ValueError as ve:
            raise HTTPException(
                status_code=422, 
                detail=f"Invalid geometry: {str(ve)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=422, 
                detail=f"Error processing geometry: {str(e)}"
            )
    
    updated = geofence_repo.update_geofence(db, geofence_id, geofence)
    
    if updated is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Geofence '{geofence_id}' not found"
        )
    
    return updated


# ==========================================================
# 📌 Delete Geofence
# ==========================================================

@router.delete("/{geofence_id}", response_model=geofence_schema.GeofenceDelete)
def delete_geofence(geofence_id: str, db: Session = Depends(get_DB)):
    """
    Delete a geofence (hard delete).
    
    Warning: This permanently removes the geofence from the database.
    Historical GPS records that reference this geofence will still
    have the geofence ID stored for audit purposes.
    
    Consider deactivating instead (PATCH with is_active=false) to:
    - Preserve audit trail
    - Allow reactivation if needed
    - Maintain referential integrity
    
    Args:
        geofence_id: Unique geofence identifier
        
    Returns:
        Confirmation message:
        {
            "id": "warehouse-001",
            "status": "deleted"
        }
    
    Example Request:
        DELETE /geofences/warehouse-001
    
    Raises:
        404: Geofence not found
    
    Deactivation Alternative:
        To deactivate instead of delete, use:
        PATCH /geofences/warehouse-001
        {"is_active": false}
    
    Impact on GPS Data:
        - Existing GPS records keep their CurrentGeofenceID/Name
        - Future GPS data will not detect this geofence
        - Historical reports remain accurate
    """
    success = geofence_repo.delete_geofence(db, geofence_id)
    
    if not success:
        raise HTTPException(
            status_code=404, 
            detail=f"Geofence '{geofence_id}' not found"
        )
    
    return {
        "id": geofence_id,
        "status": "deleted"
    }


# ==========================================================
# 📌 Check Point in Geofence (Spatial Query)
# ==========================================================

@router.get("/check/point", response_model=geofence_schema.GeofenceContainmentCheck)
def check_point_in_geofence(
    latitude: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    longitude: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    db: Session = Depends(get_DB)
):
    """
    Check if a GPS point is inside any active geofences.
    
    Uses PostGIS spatial query (ST_Intersects) with GIST index for fast lookup.
    Returns all geofences that contain the point (handles overlapping geofences).
    
    Args:
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        
    Returns:
        Containment check result:
        {
            "latitude": 10.9878,
            "longitude": -74.7889,
            "inside_geofences": [
                {
                    "id": "warehouse-001",
                    "name": "Main Warehouse",
                    "type": "warehouse",
                    "is_active": true,
                    "color": "#28a745",
                    "created_at": "2025-09-01T00:00:00Z",
                    "updated_at": null
                },
                {
                    "id": "industrial-zone-1",
                    "name": "Industrial Zone",
                    "type": "zone",
                    ...
                }
            ],
            "count": 2
        }
    
    Example Requests:
        GET /geofences/check/point?latitude=10.9878&longitude=-74.7889
        GET /geofences/check/point?latitude=40.7128&longitude=-74.0060
    
    Performance:
        - Uses GIST spatial index on geometry column
        - Typical query time: <5ms for 100+ geofences
        - Returns all overlapping geofences (not just first match)
    
    Use Cases:
        - Real-time location check from frontend
        - Manual verification of geofence boundaries
        - Debugging geofence detection issues
        - Testing new geofence configurations
    
    Note:
        Only checks ACTIVE geofences (is_active=True).
        Inactive geofences are excluded from check.
    """
    geofences = geofence_repo.get_geofences_containing_point(
        db, latitude, longitude, only_active=True
    )
    
    geofences_list = [
        geofence_schema.GeofenceGet.model_validate(geofence, from_attributes=True)
        for geofence in geofences
    ]
    
    return {
        "latitude": latitude,
        "longitude": longitude,
        "inside_geofences": geofences_list,
        "count": len(geofences_list)
    }


# ==========================================================
# 📌 Bulk Import from GeoJSON File
# ==========================================================

@router.post("/import", status_code=200)
async def import_geofences(
    file: UploadFile = File(..., description="GeoJSON file with geofences"),
    mode: str = Query("skip", regex="^(skip|update|replace)$", description="Import mode"),
    db: Session = Depends(get_DB)
):
    """
    Bulk import geofences from a GeoJSON FeatureCollection file.
    
    Supports three import modes for handling existing geofences:
    - 'skip': Skip existing geofences (safest, default)
    - 'update': Update existing geofences with new data
    - 'replace': Delete and recreate existing geofences
    
    Args:
        file: GeoJSON file (multipart/form-data)
              Must be FeatureCollection with Polygon geometries
        mode: Import mode (default: "skip")
            - 'skip': Skip duplicates, only create new geofences
            - 'update': Update existing geofences, create new ones
            - 'replace': Delete existing and recreate, create new ones
        
    Returns:
        Import statistics:
        {
            "message": "Import complete",
            "created": 15,
            "updated": 3,
            "skipped": 2,
            "failed": 0
        }
    
    Example Request:
        POST /geofences/import?mode=skip
        Content-Type: multipart/form-data
        Body: geofences.geojson (file upload)
    
    GeoJSON File Format:
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "id": "warehouse-001",
                        "name": "Main Warehouse",
                        "description": "Primary storage",
                        "type": "warehouse",
                        "is_active": true,
                        "color": "#28a745",
                        "metadata": {"capacity": 5000}
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[lon, lat], ...]]
                    }
                },
                ...
            ]
        }
    
    Raises:
        400: Invalid file format (not GeoJSON)
        422: Validation errors in GeoJSON features
    
    Processing:
        1. File uploaded to temporary location
        2. GeoPandas reads and validates GeoJSON
        3. CRS reprojection to EPSG:4326 if needed
        4. Each feature validated and processed
        5. Geometries converted to PostGIS WKT
        6. Bulk insert/update with error handling
        7. Temporary file cleaned up
    
    Performance:
        - 100 geofences: ~2-5 seconds
        - 1000 geofences: ~20-30 seconds
        - Progress is logged to console
    
    Use Cases:
        - Initial system setup with many geofences
        - Bulk updates from GIS software (QGIS, ArcGIS)
        - Migration from other systems
        - Backup/restore operations
    """
    # Validate file extension
    if not file.filename.endswith(('.geojson', '.json')):
        raise HTTPException(
            status_code=400, 
            detail="File must be GeoJSON format (.geojson or .json extension)"
        )
    
    # Save uploaded file to temporary location
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.geojson') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        print(f"[GEOFENCE-IMPORT] Processing file: {file.filename} ({len(content)} bytes)")
        print(f"[GEOFENCE-IMPORT] Mode: {mode}")
        
        # Import geofences using service
        importer = GeofenceImporter(db)
        created, updated, skipped, failed = importer.import_from_file(
            str(tmp_path)
        )
        
        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {
            "message": "Import complete",
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "failed": failed
        }
        
    except Exception as e:
        # Clean up temporary file on error
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        print(f"[GEOFENCE-IMPORT] ERROR: {str(e)}")
        
        raise HTTPException(
            status_code=422, 
            detail=f"Import failed: {str(e)}"
        )