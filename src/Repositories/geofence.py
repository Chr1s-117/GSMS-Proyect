# src/Repositories/geofence.py

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
        
    Example:
        new_geofence = create_geofence(db, geofence_data)
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
        updated = update_geofence(db, "warehouse-001", update_data)
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
    Consider using deactivate_geofence() for soft delete.
    
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
# 📌 SPATIAL QUERIES (PostGIS integration)
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
    
    Args:
        db: SQLAlchemy session
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        only_active: If True, only checks active geofences (default: True)
        
    Returns:
        List of Geofence objects containing the point
        
    Example:
        geofences = get_geofences_containing_point(db, 10.9878, -74.7889)
        # Returns geofences that contain the point (10.9878, -74.7889)
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
    Useful for "nearby geofences" or proximity alerts.
    
    Args:
        db: SQLAlchemy session
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        radius_meters: Search radius in meters
        only_active: If True, only checks active geofences (default: True)
        
    Returns:
        List of Geofence objects within the specified distance
        
    Example:
        nearby = get_geofences_within_distance(db, 10.9878, -74.7889, 1000)
        # Returns geofences within 1km of the point
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
    
    Args:
        db: SQLAlchemy session
        latitude: GPS latitude (-90 to 90)
        longitude: GPS longitude (-180 to 180)
        only_active: If True, only checks active geofences (default: True)
        
    Returns:
        First Geofence object containing the point, or None if outside all geofences
        
    Example:
        current_geofence = get_first_containing_geofence(db, 10.9878, -74.7889)
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
        if geofence_exists(db, "warehouse-001"):
            print("Geofence found")
    """
    return db.query(Geofence).filter(Geofence.id == geofence_id).count() > 0


def get_geofence_types(db: Session, only_active: bool = True) -> List[str]:
    """
    Get a list of all unique geofence types in the database.
    
    Args:
        db: SQLAlchemy session
        only_active: If True, only considers active geofences (default: True)
        
    Returns:
        List of unique type strings
        
    Example:
        types = get_geofence_types(db)
        # Returns: ["warehouse", "delivery_zone", "custom"]
    """
    query = db.query(Geofence.type).distinct()
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    results = query.all()
    return [row[0] for row in results]