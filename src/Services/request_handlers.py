# src/Services/request_handlers.py
"""
Trip Query Handlers for REST API
=================================

This module contains complex trip query logic (temporal/spatial/hybrid queries)
that is reused by the REST endpoint GET /gps_data/trips.

All other handlers have been removed as they were only used by WebSocket endpoints,
which have been migrated to direct REST implementations in gps_datas.py.

Remaining handler:
- handle_get_trips: Complex multi-mode trip queries (used by GET /gps_data/trips)
"""

from typing import Dict, Any, List
from datetime import datetime
from src.DB.session import SessionLocal
from src.Repositories.gps_data import get_unique_trip_ids_near_location
from src.Repositories.trip import get_trips_in_time_range, get_trip_by_id
from src.Services.trip_assembler import trip_assembler


# ==========================================================
# RESPONSE BUILDER
# ==========================================================

def build_response(action: str, request_id: str, data: Any, status: str = "success") -> Dict[str, Any]:
    """
    Build standardized response for REST endpoints.
    
    Args:
        action: Action name (e.g., "get_trips")
        request_id: Unique request identifier
        data: Response payload
        status: "success" or "error"
        
    Returns:
        Standardized response dict
    """
    return {
        "action": action,
        "request_id": request_id,
        "status": status,
        "data": data
    }


# ==========================================================
# QUERY MODE HELPERS
# ==========================================================

def _determine_query_mode(params: Dict[str, Any]) -> str:
    """
    Determine query mode based on provided parameters.
    
    Args:
        params: Request parameters
    
    Returns:
        str: 'single_trip', 'temporal', 'spatial', or 'hybrid'
    
    Raises:
        ValueError: If parameters are invalid or missing
    """
    has_trip_id = 'trip_id' in params
    has_temporal = 'start' in params and 'end' in params
    has_spatial = 'center' in params and 'radius_meters' in params
    
    # Single trip query (highest priority)
    if has_trip_id:
        return 'single_trip'
    
    # Multi-trip queries
    if has_temporal and has_spatial:
        return 'hybrid'
    elif has_temporal:
        return 'temporal'
    elif has_spatial:
        return 'spatial'
    else:
        raise ValueError(
            "Must provide one of:\n"
            "  - 'trip_id' for single trip query\n"
            "  - 'start' + 'end' for temporal query\n"
            "  - 'center' + 'radius_meters' for spatial query\n"
            "  - All of the above for hybrid query"
        )


def _parse_datetime(value: Any, param_name: str) -> datetime:
    """
    Parse datetime from ISO string with validation.
    
    Args:
        value: DateTime value (string or datetime object)
        param_name: Parameter name for error messages
    
    Returns:
        datetime: Parsed UTC datetime
    
    Raises:
        ValueError: If parsing fails
    """
    if isinstance(value, datetime):
        return value
    
    if not isinstance(value, str):
        raise ValueError(f"Parameter '{param_name}' must be a string or datetime")
    
    try:
        # Parse ISO format, handle both with and without 'Z'
        dt_str = value.replace('Z', '+00:00')
        return datetime.fromisoformat(dt_str)
    except Exception as e:
        raise ValueError(f"Invalid datetime format for '{param_name}': {value}") from e


# ==========================================================
# TRIP ID RETRIEVAL (BY MODE)
# ==========================================================

def _get_trip_ids_single(db: Any, params: Dict[str, Any]) -> List[str]:
    """
    Get single trip ID from direct trip_id parameter.
    
    Args:
        db: SQLAlchemy session (not used, for consistency)
        params: Request parameters with 'trip_id'
    
    Returns:
        list[str]: Single-element list with the trip_id
    
    Raises:
        ValueError: If trip_id is missing or invalid
    """
    trip_id = params.get('trip_id')
    
    if not trip_id:
        raise ValueError("'trip_id' parameter is required for single trip query")
    
    if not isinstance(trip_id, str):
        raise ValueError(f"'trip_id' must be a string, got {type(trip_id).__name__}")
    
    trip_id = trip_id.strip()
    
    if not trip_id:
        raise ValueError("'trip_id' cannot be empty")
    
    print(f"[SINGLE] Requesting trip: {trip_id}")
    
    return [trip_id]


def _get_trip_ids_temporal(db: Any, params: Dict[str, Any]) -> List[str]:
    """
    Get trip IDs using temporal query (start + end).
    
    Args:
        db: SQLAlchemy session
        params: Request parameters with 'start', 'end', optional 'device_id'
    
    Returns:
        list[str]: Trip IDs matching temporal criteria
    """
    # Parse timestamps
    start_time = _parse_datetime(params['start'], 'start')
    end_time = _parse_datetime(params['end'], 'end')
    
    # Validate time range
    if start_time >= end_time:
        raise ValueError("'start' must be before 'end'")
    
    # Optional filters
    device_id = params.get('device_id')
    
    # Query trips
    trips = get_trips_in_time_range(
        db,
        start_time=start_time,
        end_time=end_time,
        device_id=device_id
    )
    
    return [str(trip.trip_id) for trip in trips]


def _get_trip_ids_spatial(db: Any, params: Dict[str, Any]) -> List[str]:
    """
    Get trip IDs using spatial query (center + radius).
    
    Uses 3-filter algorithm:
    1. Bounding box (fast)
    2. Haversine distance (accurate)
    3. Extract unique trip_ids
    
    Args:
        db: SQLAlchemy session
        params: Request parameters with 'center', 'radius_meters', optional 'device_id'
    
    Returns:
        list[str]: Trip IDs matching spatial criteria
    """
    # Validate center parameter
    center = params.get('center')
    if not isinstance(center, dict):
        raise ValueError("'center' must be an object with 'lat' and 'lon' keys")
    
    if 'lat' not in center or 'lon' not in center:
        raise ValueError("'center' must have 'lat' and 'lon' keys")
    
    # Extract and validate coordinates
    try:
        center_lat = float(center['lat'])
        center_lon = float(center['lon'])
    except (ValueError, TypeError) as e:
        raise ValueError("'center.lat' and 'center.lon' must be numbers") from e
    
    # Validate coordinate ranges
    if not (-90 <= center_lat <= 90):
        raise ValueError(f"'center.lat' must be between -90 and 90, got {center_lat}")
    
    if not (-180 <= center_lon <= 180):
        raise ValueError(f"'center.lon' must be between -180 and 180, got {center_lon}")
    
    # Validate radius
    try:
        radius_meters = float(params['radius_meters'])
    except (ValueError, TypeError) as e:
        raise ValueError("'radius_meters' must be a number") from e
    
    if radius_meters <= 0:
        raise ValueError(f"'radius_meters' must be positive, got {radius_meters}")
    
    if radius_meters > 100000:  # 100km limit
        raise ValueError(f"'radius_meters' must be <= 100000 (100km), got {radius_meters}")
    
    # Optional filters
    device_id = params.get('device_id')
    
    # Optional temporal filters for spatial query
    start_time = None
    end_time = None
    if 'start' in params:
        start_time = _parse_datetime(params['start'], 'start')
    if 'end' in params:
        end_time = _parse_datetime(params['end'], 'end')
    
    # Execute 3-filter spatial algorithm
    trip_ids = get_unique_trip_ids_near_location(
        db,
        center_lat=center_lat,
        center_lon=center_lon,
        radius_meters=radius_meters,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time
    )
    
    return trip_ids


def _get_trip_ids_hybrid(db: Any, params: Dict[str, Any]) -> List[str]:
    """
    Get trip IDs using hybrid query (temporal AND spatial).
    
    Returns intersection of temporal and spatial results.
    
    Args:
        db: SQLAlchemy session
        params: Request parameters with all temporal and spatial parameters
    
    Returns:
        list[str]: Trip IDs matching BOTH temporal AND spatial criteria
    """
    # Get temporal results
    temporal_trip_ids = set(_get_trip_ids_temporal(db, params))
    
    print(f"[HYBRID] Temporal query: {len(temporal_trip_ids)} trips")
    
    # Get spatial results
    spatial_trip_ids = set(_get_trip_ids_spatial(db, params))
    
    print(f"[HYBRID] Spatial query: {len(spatial_trip_ids)} trips")
    
    # Intersect results
    matching_trip_ids = temporal_trip_ids & spatial_trip_ids
    
    print(f"[HYBRID] Intersection: {len(matching_trip_ids)} trips")
    
    return list(matching_trip_ids)


# ==========================================================
# PUBLIC HANDLER
# ==========================================================

def handle_get_trips(params: Dict[str, Any], request_id: str) -> dict:
    """
    Unified handler for trip queries.
    
    Supports 4 query modes:
    1. SINGLE: trip_id
    2. TEMPORAL: start + end (time range)
    3. SPATIAL: center + radius_meters (location proximity)
    4. HYBRID: start + end + center + radius_meters (both filters)
    
    Optional filter: device_id (for all modes)
    
    Args:
        params: Request parameters (see mode descriptions above)
        request_id: Unique request identifier
    
    Returns:
        dict: Standardized response with trips data and summary
    
    Example Usage:
        # From REST endpoint
        result = handle_get_trips(
            params={
                'start': '2025-01-12T00:00:00Z',
                'end': '2025-01-12T23:59:59Z',
                'device_id': 'TRUCK-001'
            },
            request_id='http_request'
        )
        
        if result['status'] == 'success':
            return result['data']
        else:
            raise HTTPException(400, result['data']['error'])
    """
    try:
        # ========================================
        # STEP 1: Validate and determine query mode
        # ========================================
        mode = _determine_query_mode(params)
        
        print(f"[GET_TRIPS] Query mode: {mode}")
        if 'device_id' in params:
            print(f"[GET_TRIPS] Device filter: {params['device_id']}")
        
        # ========================================
        # STEP 2: Get trip IDs based on mode
        # ========================================
        with SessionLocal() as db:
            if mode == 'single_trip':
                trip_ids = _get_trip_ids_single(db, params)
            elif mode == 'temporal':
                trip_ids = _get_trip_ids_temporal(db, params)
            elif mode == 'spatial':
                trip_ids = _get_trip_ids_spatial(db, params)
            elif mode == 'hybrid':
                trip_ids = _get_trip_ids_hybrid(db, params)
            else:
                raise ValueError(f"Invalid query mode: {mode}")
            
            print(f"[GET_TRIPS] Found {len(trip_ids)} matching trips")
            
            # ========================================
            # STEP 3: Load complete Trip objects
            # ========================================
            trips = []
            for trip_id in trip_ids:
                trip = get_trip_by_id(db, trip_id)
                if trip:
                    trips.append(trip)
            
            if len(trips) != len(trip_ids):
                print(f"[GET_TRIPS] Warning: {len(trip_ids) - len(trips)} trip IDs not found in DB")
            
            # ========================================
            # STEP 4: Assemble complete JSON response
            # ========================================
            data = trip_assembler.build_trips_response(db, trips)
        
        print(f"[GET_TRIPS] Response ready: {data['summary']['total_trips']} trips, "
              f"{data['summary']['total_points']} points")
        
        return build_response("get_trips", request_id, data)
    
    except ValueError as ve:
        # Parameter validation errors
        print(f"[GET_TRIPS] Validation error: {ve}")
        return build_response(
            "get_trips",
            request_id,
            {"error": str(ve)},
            status="error"
        )
    
    except Exception as e:
        # Unexpected errors
        print(f"[GET_TRIPS] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return build_response(
            "get_trips",
            request_id,
            {"error": f"Internal server error: {str(e)}"},
            status="error"
        )
