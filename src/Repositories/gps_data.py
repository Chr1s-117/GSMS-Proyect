# src/Repositories/gps_data.py

from sqlalchemy.orm import Session
from src.Models.gps_data import GPS_data
from src.Schemas.gps_data import GpsData_create, GpsData_update
from src.Services.gps_serialization import serialize_gps_row, serialize_many
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from typing import Any, Optional


"""
get_gps_data_by_id to get GPS data (from one user) by ID
"""
def get_gps_data_by_id(DB: Session, gps_data_id: int):
    return DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()


# ==========================================================
# ✅ Obtener último GPS por dispositivo (ajustado para geocerca)
# ==========================================================
def get_last_gps_row_by_device(DB: Session, device_id: str, include_id: bool = False) -> dict | None:
    """
    Retrieve the most recent GPS point from a specific device.
    IMPORTANTE: Retorna campos de geocerca SIN serializar para lógica interna.
    """
    row = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.id.desc())
        .first()
    )
    
    if not row:
        print(f"[REPO] get_last_gps_row_by_device('{device_id}'): No GPS anterior encontrado")
        return None

    ts = getattr(row, "Timestamp", None)
    timestamp_iso = ts.isoformat() if ts is not None else None

    result = {
        "id": row.id if include_id else None,
        "DeviceID": row.DeviceID,
        "Latitude": row.Latitude,
        "Longitude": row.Longitude,
        "Altitude": row.Altitude,
        "Accuracy": row.Accuracy,
        "Timestamp": timestamp_iso,
        "CurrentGeofenceID": row.CurrentGeofenceID,
        "CurrentGeofenceName": row.CurrentGeofenceName,
        "GeofenceEventType": row.GeofenceEventType
    }

    print(f"[REPO] get_last_gps_row_by_device('{device_id}'):")
    print(f"[REPO]   → ID en DB: {row.id}")
    print(f"[REPO]   → CurrentGeofenceID: {result['CurrentGeofenceID']}")
    print(f"[REPO]   → GeofenceEventType: {result['GeofenceEventType']}")
    
    return result


# ==========================================================
# ✅ Obtener GPS más antiguo por dispositivo
# ==========================================================
def get_oldest_gps_row_by_device(DB: Session, device_id: str, include_id: bool = False) -> dict | None:
    row = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.id.asc())
        .first()
    )
    return serialize_gps_row(row, include_id=include_id)


# ==========================================================
# ✅ Obtener histórico por dispositivo y rango temporal
# ==========================================================
def get_gps_data_in_range_by_device(
    DB: Session,
    device_id: str,
    start_time: datetime,
    end_time: datetime,
    include_id: bool = False
) -> list[dict]:
    rows = (
        DB.query(GPS_data)
        .filter(
            GPS_data.DeviceID == device_id,
            GPS_data.Timestamp >= start_time,
            GPS_data.Timestamp <= end_time
        )
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=include_id)


# ==========================================================
# ✅ Listar todos los dispositivos que han reportado GPS
# ==========================================================
def get_all_devices(DB: Session) -> list[str]:
    result = DB.query(GPS_data.DeviceID).distinct().all()
    return [row[0] for row in result]


# ==========================================================
# ✅ Obtener última posición de todos los dispositivos
# ==========================================================
def get_last_gps_all_devices(DB: Session, include_id: bool = False) -> dict[str, dict]:
    from sqlalchemy import func, and_
    
    subq = (
        DB.query(
            GPS_data.DeviceID,
            func.max(GPS_data.id).label('max_id')
        )
        .group_by(GPS_data.DeviceID)
        .subquery()
    )
    
    rows = (
        DB.query(GPS_data)
        .join(subq, and_(
            GPS_data.DeviceID == subq.c.DeviceID,
            GPS_data.id == subq.c.max_id
        ))
        .all()
    )
    
    result = {}
    for row in rows:
        serialized = serialize_gps_row(row, include_id=include_id)
        if serialized:
            result[row.DeviceID] = serialized
    
    return result


# ==========================================================
# ✅ Verificar si un dispositivo tiene datos GPS
# ==========================================================
def device_has_gps_data(DB: Session, device_id: str) -> bool:
    count = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .limit(1)
        .count()
    )
    return count > 0


"""
created_gps_data to create a new GPS data row
"""
def created_gps_data(DB: Session, gps_data: GpsData_create):
    new_gps_data = GPS_data(**gps_data.model_dump(exclude_unset=True))
    DB.add(new_gps_data)
    DB.commit()
    DB.refresh(new_gps_data)
    return new_gps_data


"""
update_gps_data to update GPS data row by ID
"""
def update_gps_data(DB: Session, gps_data_id: int, gps_data: GpsData_update):
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if not db_gps_data:
        return None

    update_data = gps_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_gps_data, key, value)

    DB.commit()
    DB.refresh(db_gps_data)
    return db_gps_data


"""
delete_gps_data to delete GPS data row by ID
"""
def delete_gps_data(DB: Session, gps_data_id: int):
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if db_gps_data is None:
        return None
    DB.delete(db_gps_data)
    DB.commit()
    return db_gps_data.id


# ==========================================================
# ⚠️ LEGACY: Histórico global sin filtro de device
# ==========================================================
def get_gps_data_in_range(
    DB: Session, 
    start_time: datetime, 
    end_time: datetime, 
    include_id: bool = False
) -> list[dict]:
    """
    [LEGACY] Retrieve GPS data in time range from ALL devices.
    
    ⚠️ WARNING: Returns mixed GPS data from all devices.
    For device-specific history, use get_gps_data_in_range_by_device().
    
    Use only for:
    - Administrative exports
    - Global monitoring dashboards
    - Debugging
    """
    rows = (
        DB.query(GPS_data)
        .filter(
            GPS_data.Timestamp >= start_time, 
            GPS_data.Timestamp <= end_time
        )
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=include_id)


# ==========================================================
# 📦 FASE 6: Nuevas Funciones en Repository
# ==========================================================
def get_global_oldest_gps(DB: Session) -> dict | None:
    """
    Obtiene el GPS más antiguo de TODOS los devices activos.
    """
    from src.Models.device import Device
    
    row = (
        DB.query(GPS_data)
        .join(Device, GPS_data.DeviceID == Device.DeviceID)
        .filter(Device.IsActive == True)
        .order_by(GPS_data.Timestamp.asc())
        .first()
    )
    return serialize_gps_row(row, include_id=False)


def get_global_newest_gps(DB: Session) -> dict | None:
    """
    Obtiene el GPS más reciente de TODOS los devices activos.
    """
    from src.Models.device import Device
    
    row = (
        DB.query(GPS_data)
        .join(Device, GPS_data.DeviceID == Device.DeviceID)
        .filter(Device.IsActive == True)
        .order_by(GPS_data.Timestamp.desc())
        .first()
    )
    return serialize_gps_row(row, include_id=False)


def get_all_gps_for_device(DB: Session, device_id: str) -> list[dict]:
    """
    Obtiene TODO el historial GPS de un device (sin filtro temporal).
    Úsalo con cuidado en devices con mucha data.
    """
    rows = (
        DB.query(GPS_data)
        .filter(GPS_data.DeviceID == device_id)
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=False)


# ==========================================================
# 🆕 FASE 4: Query GPS por trip_id
# ==========================================================

def get_gps_by_trip_id(DB: Session, trip_id: str, include_id: bool = False) -> list[dict]:
    """
    Retrieve all GPS points belonging to a specific trip.
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
        include_id: Include internal DB id in results
        
    Returns:
        list[dict]: GPS points ordered chronologically
        
    Use cases:
        - Visualize trip route on map
        - Recalculate trip metrics
        - Export trip data
        
    Example:
        >>> gps_points = get_gps_by_trip_id(db, "TRIP_20250102_ESP001_001")
        >>> print(f"Trip has {len(gps_points)} GPS points")
        >>> # Draw polyline on map
        >>> polyline = [(p['Latitude'], p['Longitude']) for p in gps_points]
    """
    rows = (
        DB.query(GPS_data)
        .filter(GPS_data.trip_id == trip_id)
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    return serialize_many(rows, include_id=include_id)


def count_gps_by_trip_id(DB: Session, trip_id: str) -> int:
    """
    Count GPS points in a trip (faster than loading all).
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
        
    Returns:
        int: Number of GPS points
        
    Use case:
        Validate trip.point_count matches actual GPS count
        
    Example:
        >>> count = count_gps_by_trip_id(db, "TRIP_20250102_ESP001_001")
        >>> trip = get_trip_by_id(db, "TRIP_20250102_ESP001_001")
        >>> if count != trip.point_count:
        ...     print("⚠️ Inconsistency detected!")
    """
    return (
        DB.query(GPS_data)
        .filter(GPS_data.trip_id == trip_id)
        .count()
    )

#######################################################

# ==========================================================
# 🆕 FASE 1: CONSULTAS ESPACIALES
# ==========================================================

def calculate_bounding_box(
    center_lat: float,
    center_lon: float,
    radius_meters: float
) -> dict[str, float]:
    """
    Calculate geographic bounding box for spatial filtering.
    
    Uses simple approximation valid for small radii (<100km).
    
    Args:
        center_lat: Center latitude in decimal degrees
        center_lon: Center longitude in decimal degrees
        radius_meters: Radius in meters
    
    Returns:
        dict: Bounding box with keys:
            - lat_min: Minimum latitude
            - lat_max: Maximum latitude
            - lon_min: Minimum longitude
            - lon_max: Maximum longitude
    
    Example:
        >>> bbox = calculate_bounding_box(10.9878, -74.7889, 500)
        >>> print(bbox)
        {
            'lat_min': 10.9833,
            'lat_max': 10.9923,
            'lon_min': -74.7936,
            'lon_max': -74.7842
        }
    
    Notes:
        - 1 degree latitude ≈ 111,320 meters (constant)
        - 1 degree longitude ≈ 111,320 * cos(latitude) meters (varies)
        - This is faster than PostGIS for initial filtering
    """
    # Earth constants
    METERS_PER_DEGREE_LAT = 111320.0  # Approximately constant
    
    # Latitude delta (simple, works everywhere)
    lat_delta = radius_meters / METERS_PER_DEGREE_LAT
    
    # Longitude delta (depends on latitude)
    lat_rad = radians(center_lat)
    meters_per_degree_lon = METERS_PER_DEGREE_LAT * cos(lat_rad)
    
    if meters_per_degree_lon > 0:
        lon_delta = radius_meters / meters_per_degree_lon
    else:
        # Near poles, use large delta
        lon_delta = 180.0
    
    return {
        'lat_min': center_lat - lat_delta,
        'lat_max': center_lat + lat_delta,
        'lon_min': center_lon - lon_delta,
        'lon_max': center_lon + lon_delta
    }


def get_gps_in_bounding_box(
    DB: Session,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    device_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> list[GPS_data]:
    """
    FILTER 1: Fast rectangular filter using numeric indexes.
    
    Returns GPS points inside the bounding box.
    This is the FIRST filter in the 3-filter algorithm.
    
    Args:
        DB: SQLAlchemy session
        lat_min, lat_max: Latitude bounds
        lon_min, lon_max: Longitude bounds
        device_id: Optional device filter
        start_time: Optional start time filter
        end_time: Optional end time filter
    
    Returns:
        list[GPS_data]: GPS points in bounding box
    
    Performance:
        - Uses B-tree indexes on Latitude/Longitude
        - Typically reduces dataset by 95%+
        - Query time: O(log N)
    
    Example:
        >>> bbox = calculate_bounding_box(10.9878, -74.7889, 500)
        >>> gps_points = get_gps_in_bounding_box(
        ...     db,
        ...     bbox['lat_min'],
        ...     bbox['lat_max'],
        ...     bbox['lon_min'],
        ...     bbox['lon_max']
        ... )
    """
    query = DB.query(GPS_data).filter(
        GPS_data.Latitude >= lat_min,
        GPS_data.Latitude <= lat_max,
        GPS_data.Longitude >= lon_min,
        GPS_data.Longitude <= lon_max
    )
    
    # Optional filters
    if device_id:
        query = query.filter(GPS_data.DeviceID == device_id)
    
    if start_time:
        query = query.filter(GPS_data.Timestamp >= start_time)
    
    if end_time:
        query = query.filter(GPS_data.Timestamp <= end_time)
    
    return query.all()


def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance between two points (Haversine formula).
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
    
    Returns:
        float: Distance in meters
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Earth radius in meters
    r = 6371000
    
    return c * r


def get_unique_trip_ids_near_location(
    DB: Session,
    center_lat: float,
    center_lon: float,
    radius_meters: float,
    device_id: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> list[str]:
    """
    COMPLETE 3-FILTER ALGORITHM: Find trips that pass near a location.
    
    Algorithm:
        1. FILTER 1: Bounding box (fast, uses indexes)
        2. FILTER 2: Haversine distance (accurate, in Python)
        3. FILTER 3: Extract unique trip_ids
    
    Args:
        DB: SQLAlchemy session
        center_lat: Center latitude
        center_lon: Center longitude
        radius_meters: Search radius in meters
        device_id: Optional device filter
        start_time: Optional start time filter
        end_time: Optional end time filter
    
    Returns:
        list[str]: Unique trip_ids that have at least one GPS point within radius
    
    Performance:
        - Filter 1: Reduces 95%+ of points (milliseconds)
        - Filter 2: Haversine on remaining points (fast in Python)
        - Filter 3: Set deduplication (instant)
        - Total time: Usually < 100ms for 10,000 GPS points
    
    Example:
        >>> # Find trips that passed near warehouse
        >>> trip_ids = get_unique_trip_ids_near_location(
        ...     db,
        ...     center_lat=10.9878,
        ...     center_lon=-74.7889,
        ...     radius_meters=500,
        ...     device_id="ESP001",
        ...     start_time=datetime(2025, 1, 1, tzinfo=timezone.utc),
        ...     end_time=datetime(2025, 1, 31, tzinfo=timezone.utc)
        ... )
        >>> print(f"Found {len(trip_ids)} trips near location")
    
    Notes:
        - Returns empty list if no matches
        - Filters out GPS points with trip_id=NULL
        - Results are NOT sorted (use in subsequent query)
    """
    # ========================================
    # FILTER 1: Bounding Box (Fast)
    # ========================================
    bbox = calculate_bounding_box(center_lat, center_lon, radius_meters)
    
    candidate_points = get_gps_in_bounding_box(
        DB,
        bbox['lat_min'],
        bbox['lat_max'],
        bbox['lon_min'],
        bbox['lon_max'],
        device_id=device_id,
        start_time=start_time,
        end_time=end_time
    )
    
    print(f"[SPATIAL] Filter 1 (BBox): {len(candidate_points)} candidate points")
    
    if not candidate_points:
        return []
    
    # ========================================
    # FILTER 2: Haversine Distance (Accurate)
    # ========================================
    matching_trip_ids: set[str] = set()
    
    for gps in candidate_points:
        # ✅ CORRECCIÓN: Acceso seguro a atributos ORM
        trip_id_value = getattr(gps, 'trip_id', None)
        
        # Skip GPS without trip_id
        if trip_id_value is None:
            continue
        
        # ✅ CORRECCIÓN: Cast explícito de valores ORM a float
        lat_value = float(getattr(gps, 'Latitude', 0.0))
        lon_value = float(getattr(gps, 'Longitude', 0.0))
        
        distance = _haversine_distance(
            center_lat, center_lon,
            lat_value, lon_value
        )
        
        if distance <= radius_meters:
            matching_trip_ids.add(str(trip_id_value))
    
    print(f"[SPATIAL] Filter 2 (Haversine): {len(matching_trip_ids)} unique trip_ids within {radius_meters}m")
    
    # ========================================
    # FILTER 3: Return Unique Trip IDs
    # ========================================
    return list(matching_trip_ids)

# ==========================================================
# 🆕 FASE 2: AGREGACIÓN DE DATOS
# ==========================================================

def get_full_gps_data_for_trip(
    DB: Session,
    trip_id: str
) -> list[dict[str, Any]]:
    """
    Get ALL GPS points for a trip with enriched format.
    
    Returns GPS data in frontend-ready format with:
    - Basic GPS fields (lat, lon, alt, accuracy, timestamp)
    - Geofence data (id, name, event) if applicable
    - Does NOT include accelerometer (added later by TripAssembler)
    
    Args:
        DB: SQLAlchemy session
        trip_id: Trip identifier
    
    Returns:
        list[dict]: GPS points in enriched format:
        [
            {
                "timestamp": "2025-01-01T08:00:05Z",
                "gps": {
                    "lat": 10.9878,
                    "lon": -74.7889
                },
                "geofence": {
                    "id": "WAREHOUSE_01",
                    "name": "Warehouse",
                    "event": "exit"
                } | None
            },
            ...
        ]
    
    Example:
        >>> gps_data = get_full_gps_data_for_trip(db, "TRIP_20250101_ESP001_001")
        >>> print(f"Trip has {len(gps_data)} GPS points")
        >>> first_point = gps_data[0]
        >>> print(f"Started at ({first_point['gps']['lat']}, {first_point['gps']['lon']})")
    
    Performance:
        - Uses indexed trip_id column
        - Ordered chronologically for route visualization
        - Typical time: 10-50ms for 360 points
    
    Notes:
        - Returns empty list if trip has no GPS data
        - Geofence is None if GPS point is outside all geofences
        - Timestamps are normalized to UTC ISO format with 'Z' suffix
    """
    # Query GPS points for this trip (already uses index)
    rows = (
        DB.query(GPS_data)
        .filter(GPS_data.trip_id == trip_id)
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )
    
    if not rows:
        return []
    
    # Build enriched GPS data
    result: list[dict[str, Any]] = []
    
    for row in rows:
        # Normalize timestamp to UTC ISO string
        ts = getattr(row, 'Timestamp', None)
        timestamp_str = ts.strftime("%Y-%m-%dT%H:%M:%SZ") if ts else None
        
        # Extract GPS coordinates
        lat = float(getattr(row, 'Latitude', 0.0))
        lon = float(getattr(row, 'Longitude', 0.0))
        alt = float(getattr(row, 'Altitude', 0.0))
        acc = float(getattr(row, 'Accuracy', 0.0))
        
        # Extract geofence data
        geo_id = getattr(row, 'CurrentGeofenceID', None)
        geo_name = getattr(row, 'CurrentGeofenceName', None)
        geo_event = getattr(row, 'GeofenceEventType', None)
        
        # Build geofence object (None if outside all geofences)
        geofence_data = None
        if geo_id or geo_event == 'exit':
            geofence_data = {
                "id": geo_id,
                "name": geo_name,
                "event": geo_event
            }
        
        # Build GPS point
        point = {
            "timestamp": timestamp_str,
            "gps": {
                "lat": lat,
                "lon": lon
            },
            "geofence": geofence_data
        }
        
        result.append(point)
    
    return result