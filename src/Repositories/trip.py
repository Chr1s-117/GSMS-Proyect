# src/Repositories/trip.py
"""
Trip Repository - Database operations for trip management.

Responsibilities:
- CRUD operations for trips table
- Query active trips by device
- Close trips and calculate metrics
- Historical trip queries with filters

Usage:
    from src.Repositories.trip import create_trip, get_active_trip_by_device
    
    trip = create_trip(db, trip_data)
    active = get_active_trip_by_device(db, "ESP001")
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime
from typing import Optional

from src.Models.trip import Trip
from src.Schemas.trip import Trip_create, Trip_update

# ==========================================================
# CREATE OPERATIONS
# ==========================================================

def create_trip(DB: Session, trip_data: Trip_create) -> Trip:
    """
    Create a new trip record in the database.
    
    Args:
        DB: SQLAlchemy session
        trip_data: Trip_create schema with validated data
        
    Returns:
        Trip: Created trip ORM object with auto-generated fields
        
    Example:
        >>> trip = Trip_create(
        ...     trip_id="TRIP_20250102_ESP001_001",
        ...     device_id="ESP001",
        ...     trip_type="movement",
        ...     status="active",
        ...     start_time=datetime.now(timezone.utc),
        ...     start_lat=10.98,
        ...     start_lon=-74.78
        ... )
        >>> created = create_trip(db, trip)
        >>> print(created.trip_id)
        TRIP_20250102_ESP001_001
    """
    new_trip = Trip(**trip_data.model_dump(exclude_unset=True))
    DB.add(new_trip)
    DB.commit()
    DB.refresh(new_trip)  # Get auto-generated created_at
    
    print(f"[REPO] Trip created: {new_trip.trip_id} (device: {new_trip.device_id}, type: {new_trip.trip_type})")
    
    return new_trip


# ==========================================================
# READ OPERATIONS - SINGLE TRIP
# ==========================================================

def get_trip_by_id(DB: Session, trip_id: str) -> Optional[Trip]:
    """
    Retrieve a trip by its unique identifier.
    
    Args:
        DB: SQLAlchemy session
        trip_id: Unique trip identifier
        
    Returns:
        Trip or None: Trip object if found, None otherwise
    """
    return DB.query(Trip).filter(Trip.trip_id == trip_id).first()


def get_active_trip_by_device(DB: Session, device_id: str) -> Optional[Trip]:
    """
    Get the currently active trip for a specific device.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        
    Returns:
        Trip or None: Active trip if exists, None otherwise
        
    Notes:
        - A device can only have ONE active trip at a time
        - Status must be 'active'
        - Used by TripDetector to check if trip exists before creating new one
        
    Example:
        >>> active_trip = get_active_trip_by_device(db, "ESP001")
        >>> if active_trip:
        ...     print(f"Device has active {active_trip.trip_type}")
        ... else:
        ...     print("No active trip")
    """
    return (
        DB.query(Trip)
        .filter(
            Trip.device_id == device_id,
            Trip.status == 'active'
        )
        .first()
    )


# ==========================================================
# READ OPERATIONS - MULTIPLE TRIPS
# ==========================================================

def get_trips_by_device(
    DB: Session,
    device_id: str,
    status: Optional[str] = None,
    trip_type: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100
) -> list[Trip]:
    """
    Get historical trips for a device with optional filters.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        status: Filter by status ('active' or 'closed'), None for all
        trip_type: Filter by type ('movement' or 'parking'), None for all
        start_date: Filter trips starting after this datetime
        end_date: Filter trips starting before this datetime
        limit: Maximum number of trips to return (default 100)
        
    Returns:
        list[Trip]: List of trips matching filters, ordered by start_time DESC
        
    Example:
        >>> # Get last 10 closed movement trips
        >>> trips = get_trips_by_device(
        ...     db, 
        ...     device_id="ESP001",
        ...     status="closed",
        ...     trip_type="movement",
        ...     limit=10
        ... )
        >>> for trip in trips:
        ...     print(f"{trip.trip_id}: {trip.distance}m in {trip.duration}s")
    """
    query = DB.query(Trip).filter(Trip.device_id == device_id)
    
    # Optional filters
    if status:
        query = query.filter(Trip.status == status)
    
    if trip_type:
        query = query.filter(Trip.trip_type == trip_type)
    
    if start_date:
        query = query.filter(Trip.start_time >= start_date)
    
    if end_date:
        query = query.filter(Trip.start_time <= end_date)
    
    # Order by most recent first
    query = query.order_by(Trip.start_time.desc())
    
    # Limit results
    query = query.limit(limit)
    
    return query.all()


def get_all_active_trips(DB: Session) -> list[Trip]:
    """
    Get all active trips across all devices.
    
    Args:
        DB: SQLAlchemy session
        
    Returns:
        list[Trip]: All trips with status='active'
        
    Use cases:
        - Dashboard showing all vehicles in motion
        - System health monitoring
        - Cleanup operations
    """
    return (
        DB.query(Trip)
        .filter(Trip.status == 'active')
        .order_by(Trip.start_time.desc())
        .all()
    )


# ==========================================================
# UPDATE OPERATIONS
# ==========================================================

def update_trip(DB: Session, trip_id: str, trip_update: Trip_update) -> Optional[Trip]:
    """
    Update an existing trip with new data.
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
        trip_update: Trip_update schema with fields to update
        
    Returns:
        Trip or None: Updated trip if found, None otherwise
        
    Notes:
        - Only updates fields present in trip_update (exclude_unset)
        - Triggers updated_at timestamp automatically
        
    Example:
        >>> update = Trip_update(
        ...     end_time=datetime.now(timezone.utc),
        ...     status="closed",
        ...     distance=5420.5,
        ...     duration=1800.0
        ... )
        >>> trip = update_trip(db, "TRIP_20250102_ESP001_001", update)
    """
    db_trip = DB.query(Trip).filter(Trip.trip_id == trip_id).first()
    
    if not db_trip:
        print(f"[REPO] Trip not found: {trip_id}")
        return None
    
    # Update only provided fields
    update_data = trip_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_trip, key, value)
    
    DB.commit()
    DB.refresh(db_trip)
    
    print(f"[REPO] Trip updated: {trip_id} ({len(update_data)} fields)")
    
    return db_trip


def close_trip(
    DB: Session,
    trip_id: str,
    end_time: datetime,
    distance: float,
    duration: float,
    avg_speed: Optional[float] = None
) -> Optional[Trip]:
    """
    Close an active trip and calculate final metrics.
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
        end_time: UTC timestamp of trip end
        distance: Total distance in meters
        duration: Total duration in seconds
        avg_speed: Average speed in km/h (calculated if None)
        
    Returns:
        Trip or None: Closed trip if found, None otherwise
        
    Notes:
        - Sets status to 'closed'
        - Calculates avg_speed if not provided: (distance / duration) * 3.6
        - This is typically called by TripDetector when starting new trip
    """
    db_trip = DB.query(Trip).filter(Trip.trip_id == trip_id).first()
    
    if not db_trip:
        print(f"[REPO] Cannot close trip - not found: {trip_id}")
        return None
    
    # Calculate avg_speed if not provided
    if avg_speed is None and duration > 0:
        # (meters / seconds) * 3.6 = km/h
        avg_speed = (distance / duration) * 3.6
    
    # ✅ CORRECCIÓN: Usar setattr (consistente con update_trip)
    setattr(db_trip, 'status', 'closed')
    setattr(db_trip, 'end_time', end_time)
    setattr(db_trip, 'distance', distance)
    setattr(db_trip, 'duration', duration)
    setattr(db_trip, 'avg_speed', avg_speed)
    
    DB.commit()
    DB.refresh(db_trip)
    
    print(f"[REPO] Trip closed: {trip_id} - {distance:.1f}m in {duration:.0f}s ({avg_speed:.2f} km/h)")
    
    return db_trip


def increment_point_count(DB: Session, trip_id: str) -> bool:
    """
    Increment the GPS point counter for a trip.
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
        
    Returns:
        bool: True if updated, False if trip not found
        
    Notes:
        - Called by UDP service when inserting GPS with trip_id
        - Uses atomic SQL UPDATE (no race conditions)
        
    Example:
        >>> # Called when inserting GPS
        >>> increment_point_count(db, "TRIP_20250102_ESP001_001")
    """
    result = (
        DB.query(Trip)
        .filter(Trip.trip_id == trip_id)
        .update(
            {Trip.point_count: Trip.point_count + 1},
            synchronize_session=False
        )
    )
    
    DB.commit()
    
    if result > 0:
        print(f"[REPO] Trip {trip_id}: point_count incremented")
        return True
    else:
        print(f"[REPO] Cannot increment - trip not found: {trip_id}")
        return False


# ==========================================================
# DELETE OPERATIONS
# ==========================================================

def delete_trip(DB: Session, trip_id: str) -> bool:
    """
    Delete a trip from the database.
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
        
    Returns:
        bool: True if deleted, False if not found
        
    Notes:
        - GPS points with this trip_id will have trip_id set to NULL (ON DELETE SET NULL)
        - Use with caution - prefer closing trips instead of deleting
        
    Warning:
        This is a destructive operation. Historical data is lost.
        Consider archiving before deletion.
    """
    db_trip = DB.query(Trip).filter(Trip.trip_id == trip_id).first()
    
    if not db_trip:
        print(f"[REPO] Cannot delete - trip not found: {trip_id}")
        return False
    
    DB.delete(db_trip)
    DB.commit()
    
    print(f"[REPO] Trip deleted: {trip_id}")
    
    return True


# ==========================================================
# AGGREGATION QUERIES
# ==========================================================

def get_trip_statistics_by_device(
    DB: Session,
    device_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> dict:
    """
    Get aggregated statistics for a device's trips.
    
    Args:
        DB: SQLAlchemy session
        device_id: Device identifier
        start_date: Filter trips starting after this datetime
        end_date: Filter trips starting before this datetime
        
    Returns:
        dict: Statistics with keys:
            - total_trips: Total number of trips
            - movement_trips: Number of movement trips
            - parking_sessions: Number of parking sessions
            - total_distance: Sum of all distances (meters)
            - total_duration: Sum of all durations (seconds)
            - avg_speed: Average speed across all trips (km/h)
    """
    query = DB.query(
        func.count(Trip.trip_id).label('total_trips'),
        func.count(Trip.trip_id).filter(Trip.trip_type == 'movement').label('movement_trips'),
        func.count(Trip.trip_id).filter(Trip.trip_type == 'parking').label('parking_sessions'),
        func.sum(Trip.distance).label('total_distance'),
        func.sum(Trip.duration).label('total_duration'),
        func.avg(Trip.avg_speed).label('avg_speed')
    ).filter(
        Trip.device_id == device_id,
        Trip.status == 'closed'  # Only closed trips have valid metrics
    )
    
    # Optional date filters
    if start_date:
        query = query.filter(Trip.start_time >= start_date)
    
    if end_date:
        query = query.filter(Trip.start_time <= end_date)
    
    result = query.first()
    
    # ✅ CORRECCIÓN: Verificar si result es None
    if result is None:
        return {
            'total_trips': 0,
            'movement_trips': 0,
            'parking_sessions': 0,
            'total_distance': 0.0,
            'total_duration': 0.0,
            'avg_speed': 0.0
        }
    
    return {
        'total_trips': result.total_trips or 0,
        'movement_trips': result.movement_trips or 0,
        'parking_sessions': result.parking_sessions or 0,
        'total_distance': result.total_distance or 0.0,
        'total_duration': result.total_duration or 0.0,
        'avg_speed': result.avg_speed or 0.0
    }
    
# ==========================================================
# 🆕 FASE 1: CONSULTAS TEMPORALES
# ==========================================================

def get_trips_in_time_range(
    DB: Session,
    start_time: datetime,
    end_time: datetime,
    device_id: Optional[str] = None,
    trip_type: Optional[str] = None,
    status: Optional[str] = None
) -> list[Trip]:
    """
    Retrieve trips that OVERLAP with the given time range.
    
    Overlapping Logic:
    - Trip starts BEFORE end_time (trip.start_time < end_time)
    - Trip ends AFTER start_time OR is still active (trip.end_time > start_time OR trip.end_time IS NULL)
    
    Args:
        DB: SQLAlchemy session
        start_time: Start of time range (UTC)
        end_time: End of time range (UTC)
        device_id: Optional device filter
        trip_type: Optional filter ('movement' or 'parking')
        status: Optional filter ('active' or 'closed')
    
    Returns:
        list[Trip]: Trips that overlap with the time range
    
    Examples:
        >>> # All trips in January 2025
        >>> trips = get_trips_in_time_range(
        ...     db,
        ...     datetime(2025, 1, 1, tzinfo=timezone.utc),
        ...     datetime(2025, 1, 31, 23, 59, 59, tzinfo=timezone.utc)
        ... )
        
        >>> # Only movement trips for specific device
        >>> trips = get_trips_in_time_range(
        ...     db,
        ...     start_time,
        ...     end_time,
        ...     device_id="ESP001",
        ...     trip_type="movement"
        ... )
    
    Notes:
        - Active trips (end_time=NULL) are always included if they started before end_time
        - Uses indexed columns for optimal performance
        - Ordered by start_time DESC (most recent first)
    """

    # Base query
    query = DB.query(Trip).filter(
        Trip.start_time < end_time  # Trip started before range ends
    )
    
    # Overlapping condition: Trip ends after range starts OR is still active
    query = query.filter(
        or_(
            Trip.end_time > start_time,
            Trip.end_time.is_(None)  # Active trips
        )
    )
    
    # Optional filters
    if device_id:
        query = query.filter(Trip.device_id == device_id)
    
    if trip_type:
        query = query.filter(Trip.trip_type == trip_type)
    
    if status:
        query = query.filter(Trip.status == status)
    
    # Order by most recent first
    query = query.order_by(Trip.start_time.desc())
    
    return query.all()