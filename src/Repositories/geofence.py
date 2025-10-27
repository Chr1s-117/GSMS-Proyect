# src/Repositories/geofence.py

"""
Geofence Repository Module

This module provides database access functions for Geofence model operations,
including PostGIS spatial queries for point-in-polygon and proximity detection.

Responsibilities:
- CRUD operations for geofences
- PostGIS spatial queries (ST_Contains, ST_DWithin)
- Geofence validation and existence checks
- Geofence statistics and filtering

PostGIS Requirements:
    - PostgreSQL with PostGIS extension enabled
    - Spatial index on geometry column (GIST index)
    - SRID 4326 (WGS84) coordinate system

Usage:
    from src.Repositories import geofence as geofence_repo
    from src.DB.session import SessionLocal
    
    db = SessionLocal()
    
    # Check if GPS point is inside any geofence
    geofences = geofence_repo.get_geofences_containing_point(
        db, latitude=10.9878, longitude=-74.7889
    )
    
    if geofences:
        print(f"Point is inside: {geofences[0].name}")

Performance Considerations:
    - Spatial queries use GIST index on geometry column
    - For high-frequency queries, consider caching active geofences in memory
    - Use get_first_containing_geofence() when you only need one geofence
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.functions import ST_Contains, ST_DWithin, ST_GeogFromText
from src.Models.geofence import Geofence
from src.Schemas.geofence import GeofenceCreate, GeofenceUpdate
from typing import List, Optional


# ==========================================================
# 📌 BASIC CRUD OPERATIONS
# ==========================================================

def get_all_geofences(db: Session, only_active: bool = True) -> List[Geofence]:
    """
    Get all geofences from the database.
    
    Args:
        db: SQLAlchemy session
        only_active: If True, returns only active geofences (default: True)
        
    Returns:
        List of Geofence objects
        
    Example:
        active_geofences = get_all_geofences(db, only_active=True)
        all_geofences = get_all_geofences(db, only_active=False)
    """
    query = db.query(Geofence)
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.all()


def get_geofence_by_id(db: Session, geofence_id: str) -> Optional[Geofence]:
    """
    Get a specific geofence by its ID.
    
    Args:
        db: SQLAlchemy session
        geofence_id: Unique identifier of the geofence
        
    Returns:
        Geofence object or None if not found
        
    Example:
        geofence = get_geofence_by_id(db, "warehouse-001")
        if geofence:
            print(f"Geofence found: {geofence.name}")
    """
    return db.query(Geofence).filter(Geofence.id == geofence_id).first()


def create_geofence(db: Session, geofence: GeofenceCreate) -> Geofence:
    """
    Create a new geofence.
    
    Args:
        db: SQLAlchemy session
        geofence: Geofence data (Pydantic schema)
        
    Returns:
        Created Geofence object
        
    Raises:
        IntegrityError: If geofence_id already exists (duplicate)
        
    Example:
        from shapely.geometry import Polygon
        from geoalchemy2.shape import from_shape
        
        polygon = Polygon([
            (-74.006, 40.7128),
            (-74.005, 40.7128),
            (-74.005, 40.7138),
            (-74.006, 40.7138),
            (-74.006, 40.7128)
        ])
        
        new_geofence = create_geofence(db, GeofenceCreate(
            id="warehouse-001",
            name="Main Warehouse",
            geometry=from_shape(polygon, srid=4326),
            type="warehouse"
        ))
    """
    geofence_dict = geofence.model_dump(exclude_unset=True)
    new_geofence = Geofence(**geofence_dict)
    db.add(new_geofence)
    db.commit()
    db.refresh(new_geofence)
    return new_geofence


def update_geofence(
    db: Session, 
    geofence_id: str, 
    geofence: GeofenceUpdate
) -> Optional[Geofence]:
    """
    Update an existing geofence.
    
    Args:
        db: SQLAlchemy session
        geofence_id: ID of the geofence to update
        geofence: Fields to update (Pydantic schema)
        
    Returns:
        Updated Geofence object or None if not found
        
    Example:
        updated = update_geofence(db, "warehouse-001", GeofenceUpdate(
            name="Updated Warehouse Name",
            color="#FF5733"
        ))
        
    Note: Updating geometry will require reprocessing all current GPS points
          to recalculate geofence containment.
    """
    db_geofence = get_geofence_by_id(db, geofence_id)
    
    if not db_geofence:
        return None
    
    # Only update fields that were provided
    update_data = geofence.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_geofence, key):
            setattr(db_geofence, key, value)
    
    db.commit()
    db.refresh(db_geofence)
    return db_geofence


def delete_geofence(db: Session, geofence_id: str) -> bool:
    """
    Delete a geofence (hard delete).
    
    ⚠️ WARNING: This permanently removes the geofence from the database.
    Consider using deactivate_geofence() for soft delete to preserve historical data.
    
    Args:
        db: SQLAlchemy session
        geofence_id: ID of the geofence to delete
        
    Returns:
        True if deleted successfully, False if not found
        
    Example:
        success = delete_geofence(db, "warehouse-001")
    """
    db_geofence = get_geofence_by_id(db, geofence_id)
    
    if not db_geofence:
        return False
    
    db.delete(db_geofence)
    db.commit()
    return True


def deactivate_geofence(db: Session, geofence_id: str) -> bool:
    """
    Deactivate a geofence (soft delete).
    
    This preserves the geofence data while marking it as inactive.
    Recommended over hard delete for maintaining historical data integrity.
    GPS records will still reference this geofence_id in CurrentGeofenceID field.
    
    Args:
        db: SQLAlchemy session
        geofence_id: ID of the geofence to deactivate
        
    Returns:
        True if deactivated successfully, False if not found
        
    Example:
        success = deactivate_geofence(db, "warehouse-001")
    """
    db_geofence = get_geofence_by_id(db, geofence_id)
    
    if not db_geofence:
        return False
    
    db_geofence.is_active = False
    db.commit()
    return True


def count_geofences(db: Session, only_active: bool = True) -> int:
    """
    Count geofences in the database.
    
    Args:
        db: SQLAlchemy session
        only_active: If True, counts only active geofences (default: True)
        
    Returns:
        Number of geofences
        
    Example:
        total_active = count_geofences(db, only_active=True)
        total_all = count_geofences(db, only_active=False)
    """
    query = db.query(Geofence)
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.count()


# ==========================================================
# 📌 SPATIAL QUERIES (PostGIS integration) - CRITICAL
# ==========================================================

def get_geofences_containing_point(
    db: Session, 
    latitude: float, 
    longitude: float,
    only_active: bool = True
) -> List[Geofence]:
    """
    Get all geofences that contain a specific GPS point.
    
    Uses PostGIS ST_Contains for spatial query.
    Utilizes spatial index (idx_geofences_geometry) for performance.
    
    THIS IS THE CORE FUNCTION FOR GEOFENCE DETECTION.
    Called every time a GPS point is received to determine if device
    has entered/exited/stayed inside a geofence.
    
    Args:
        db: SQLAlchemy session
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        only_active: If True, only checks active geofences (default: True)
        
    Returns:
        List of Geofence objects containing the point
        
    Example:
        geofences = get_geofences_containing_point(db, 10.9878, -74.7889)
        if geofences:
            print(f"Point is inside {len(geofences)} geofence(s)")
            for gf in geofences:
                print(f"  - {gf.name} ({gf.type})")
        else:
            print("Point is outside all geofences")
    
    Performance:
        - Uses GIST spatial index on geometry column
        - Average query time: <10ms for 100 geofences
        - Complexity: O(log n) with spatial index
    
    PostGIS Function Used:
        ST_Contains(geofence_polygon, gps_point) → boolean
        
    WKT Format Note:
        POINT(longitude latitude) - Note the order is lon, lat (NOT lat, lon)!
        This follows the GeoJSON standard.
    """
    # WKT format: POINT(longitude latitude) - Note the order!
    point_wkt = f'POINT({longitude} {latitude})'
    
    query = db.query(Geofence).filter(
        func.ST_Contains(
            Geofence.geometry,
            func.ST_GeogFromText(point_wkt)
        )
    )
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.all()


def get_geofences_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: float,
    only_active: bool = True
) -> List[Geofence]:
    """
    Get all geofences within a certain distance from a point.
    
    Uses PostGIS ST_DWithin for spatial query.
    Useful for:
    - "Nearby geofences" features
    - Proximity alerts (e.g., "approaching warehouse")
    - Predictive geofence detection
    
    Args:
        db: SQLAlchemy session
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        radius_meters: Search radius in meters
        only_active: If True, only checks active geofences (default: True)
        
    Returns:
        List of Geofence objects within the specified distance
        
    Example:
        # Find geofences within 1km
        nearby = get_geofences_within_distance(db, 10.9878, -74.7889, 1000)
        
        for gf in nearby:
            print(f"Nearby: {gf.name} (within 1km)")
    
    Performance:
        - Uses GIST spatial index
        - Faster than distance calculation + filtering
        - Average query time: <15ms for 100 geofences with 1km radius
    
    PostGIS Function Used:
        ST_DWithin(geofence, point, distance_meters) → boolean
    """
    # WKT format: POINT(longitude latitude)
    point_wkt = f'POINT({longitude} {latitude})'
    
    query = db.query(Geofence).filter(
        func.ST_DWithin(
            Geofence.geometry,
            func.ST_GeogFromText(point_wkt),
            radius_meters
        )
    )
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.all()


def get_geofences_by_type(
    db: Session, 
    geofence_type: str,
    only_active: bool = True
) -> List[Geofence]:
    """
    Get all geofences of a specific type.
    
    Args:
        db: SQLAlchemy session
        geofence_type: Type of geofence (e.g., "warehouse", "delivery_zone", "custom")
        only_active: If True, only returns active geofences (default: True)
        
    Returns:
        List of Geofence objects matching the type
        
    Example:
        warehouses = get_geofences_by_type(db, "warehouse")
        for warehouse in warehouses:
            print(f"Warehouse: {warehouse.name}")
    """
    query = db.query(Geofence).filter(Geofence.type == geofence_type)
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.all()


def get_first_containing_geofence(
    db: Session,
    latitude: float,
    longitude: float,
    only_active: bool = True
) -> Optional[Geofence]:
    """
    Get the first geofence that contains a specific GPS point.
    
    Useful when you only need to know if a point is inside ANY geofence,
    not all of them (performance optimization).
    
    Use Cases:
    - Quick containment check (is point inside or outside?)
    - Single geofence assignment (assign device to first matching zone)
    - Performance optimization when multiple geofences don't matter
    
    Args:
        db: SQLAlchemy session
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        only_active: If True, only checks active geofences (default: True)
        
    Returns:
        First Geofence object containing the point, or None if outside all geofences
        
    Example:
        current_geofence = get_first_containing_geofence(db, 10.9878, -74.7889)
        if current_geofence:
            print(f"Device is in: {current_geofence.name}")
        else:
            print("Device is outside all geofences")
    
    Performance:
        - Faster than get_geofences_containing_point() because stops at first match
        - Best case: O(1) if first geofence in index matches
        - Worst case: Same as get_geofences_containing_point()
    """
    point_wkt = f'POINT({longitude} {latitude})'
    
    query = db.query(Geofence).filter(
        func.ST_Contains(
            Geofence.geometry,
            func.ST_GeogFromText(point_wkt)
        )
    )
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.first()


# ==========================================================
# 📌 UTILITY FUNCTIONS
# ==========================================================

def geofence_exists(db: Session, geofence_id: str) -> bool:
    """
    Check if a geofence exists in the database.
    
    Args:
        db: SQLAlchemy session
        geofence_id: ID to check
        
    Returns:
        True if geofence exists, False otherwise
        
    Example:
        if not geofence_exists(db, "warehouse-001"):
            raise HTTPException(404, "Geofence not found")
    """
    return db.query(Geofence).filter(Geofence.id == geofence_id).count() > 0


def get_geofence_types(db: Session, only_active: bool = True) -> List[str]:
    """
    Get a list of all unique geofence types in the database.
    
    Useful for:
    - Populating filter dropdowns in UI
    - Statistics dashboards
    - Validation of geofence type field
    
    Args:
        db: SQLAlchemy session
        only_active: If True, only considers active geofences (default: True)
        
    Returns:
        List of unique type strings
        
    Example:
        types = get_geofence_types(db)
        # Returns: ["warehouse", "delivery_zone", "custom", "parking"]
        
        # Use in dropdown
        for type_name in types:
            print(f"<option value='{type_name}'>{type_name}</option>")
    """
    query = db.query(Geofence.type).distinct()
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    results = query.all()
    return [row[0] for row in results]