# src/Controller/Routes/gps_datas.py
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.Controller.deps import get_DB
from src.Repositories import gps_data as gps_data_repo
from src.Schemas import gps_data as gps_data_schema

router = APIRouter()

# ==========================================================
# ✅ SPECIAL GET ROUTES (Specific routes - PRIORITY ORDER)
# ==========================================================
# These endpoints must be defined BEFORE any route with path parameters
# to prevent FastAPI from misinterpreting specific paths as variable captures.
#
# Order matters: /specific/path must come before /{variable}
# ==========================================================

@router.get("/devices", response_model=dict)
def get_all_devices(DB: Session = Depends(get_DB)):
    """
    Get a list of all unique DeviceIDs that have reported GPS data.
    
    Useful for populating device selection dropdowns in the frontend.
    
    Returns:
        {
            "devices": ["TRUCK-001", "TRUCK-002", "TEST-DEVICE-001"],
            "count": 3
        }
    
    Example:
        GET /gps_data/devices
    """
    devices = gps_data_repo.get_all_devices(DB)
    
    return {
        "devices": devices,
        "count": len(devices)
    }


@router.get("/last", response_model=gps_data_schema.GpsData_get)
def get_last_gps_row(
    device_id: str = Query(..., description="Device ID (required)"),
    DB: Session = Depends(get_DB)
):
    """
    Get the most recent GPS record for a specific device.
    
    Args:
        device_id: Device identifier (required)
        
    Returns:
        Latest GPS record for the specified device
        
    Example:
        GET /gps_data/last?device_id=TRUCK-001
    
    Raises:
        404: No GPS data found for the specified device
    """
    last_row = gps_data_repo.get_last_gps_row_by_device(DB, device_id, include_id=True)
    
    if last_row is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No GPS data found for device '{device_id}'"
        )
    
    return last_row


@router.get("/oldest", response_model=gps_data_schema.GpsData_get)
def get_oldest_gps_row(
    device_id: str = Query(..., description="Device ID (required)"),
    DB: Session = Depends(get_DB)
):
    """
    Get the oldest GPS record for a specific device (starting point of route history).
    
    Args:
        device_id: Device identifier (required)
        
    Returns:
        Oldest GPS record for the specified device
        
    Example:
        GET /gps_data/oldest?device_id=TRUCK-001
    
    Raises:
        404: No GPS data found for the specified device
    """
    oldest_row = gps_data_repo.get_oldest_gps_row_by_device(DB, device_id, include_id=True)
    
    if oldest_row is None:
        raise HTTPException(
            status_code=404, 
            detail=f"No GPS data found for device '{device_id}'"
        )
    
    return oldest_row


@router.get("/range", response_model=List[gps_data_schema.GpsData_get])
def get_gps_data_range(
    start: datetime = Query(..., description="Start timestamp in ISO-8601 UTC"),
    end: datetime = Query(..., description="End timestamp in ISO-8601 UTC"),
    device_id: str = Query(None, description="Optional: Filter by specific device"),
    DB: Session = Depends(get_DB)
):
    """
    Get GPS data within a time range.
    
    Modes:
    - With device_id: Returns GPS only from the specified device (recommended)
    - Without device_id: Returns GPS from ALL devices (for global queries/exports)
    
    Args:
        start: Start of time range (inclusive, UTC)
        end: End of time range (inclusive, UTC)
        device_id: Optional device identifier to filter by
        
    Returns:
        List of GPS records ordered chronologically
        
    Examples:
        GET /gps_data/range?start=2025-10-11T00:00:00Z&end=2025-10-12T23:59:59Z&device_id=TRUCK-001
        GET /gps_data/range?start=2025-10-11T00:00:00Z&end=2025-10-12T23:59:59Z
    
    Raises:
        404: No GPS data found in range
    """
    if device_id:
        # Get GPS from specific device within range
        data = gps_data_repo.get_gps_data_in_range_by_device(
            DB, device_id, start, end, include_id=True
        )
    else:
        # Get GPS from all devices within range (for global queries)
        data = gps_data_repo.get_gps_data_in_range(DB, start, end, include_id=True)
    
    if not data:
        if device_id:
            raise HTTPException(
                status_code=404, 
                detail=f"No GPS data found for device '{device_id}' in the specified time range"
            )
        else:
            raise HTTPException(
                status_code=404, 
                detail="No GPS data found in the specified time range"
            )
    
    return data


# ==========================================================
# ✨ NEW REST ENDPOINTS - MIGRATION FROM WEBSOCKET
# ==========================================================
# These endpoints replace WebSocket actions with proper REST APIs
# for improved scalability, HTTP caching, and maintainability.
#
# Migration Map:
#   WS: get_last_positions    → GET /positions/latest
#   WS: get_timestamp_range   → GET /timestamps/range
#   WS: get_history           → GET /history
#   WS: get_trips             → GET /trips
#
# IMPORTANT: These must be defined BEFORE /{gps_data_id} to avoid
# FastAPI routing conflicts (specific paths before variable paths).
# ==========================================================

@router.get("/positions/latest", response_model=dict)
def get_latest_positions(
    DB: Session = Depends(get_DB)
):
    """
    Get the most recent GPS position for all active devices.
    
    **REPLACES**: WebSocket action 'get_last_positions'
    
    **Purpose**: 
    Used by frontend for real-time tracking map updates (polling every 5 seconds).
    
    **Returns**:
```json
    {
        "positions": {
            "DEVICE_001": {
                "DeviceID": "DEVICE_001",
                "Latitude": 10.9878,
                "Longitude": -74.7889,
                "Altitude": 100.0,
                "Accuracy": 5.0,
                "Timestamp": "2025-01-12T10:30:00Z",
                "geofence": {
                    "id": "WAREHOUSE_01",
                    "name": "Main Warehouse",
                    "event": "inside"
                }
            },
            "DEVICE_002": { ... }
        },
        "count": 2,
        "timestamp": "2025-01-12T10:30:05Z"
    }
```
    
    **Performance**:
    - Single optimized DB query
    - Typical response time: 10-20ms
    - Designed for HTTP caching (Phase 2)
    
    **HTTP Status Codes**:
    - 200: Success (positions returned)
    - 500: Database error
    """
    from datetime import datetime, timezone
    
    try:
        # Query DB for latest positions (reuses existing repository function)
        positions = gps_data_repo.get_last_gps_all_devices(DB, include_id=False)
        
        # Build response
        result = {
            "positions": positions,
            "count": len(positions),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch latest positions: {str(e)}"
        )


@router.get("/timestamps/range", response_model=dict)
def get_timestamp_range(
    device_id: Optional[str] = Query(None, description="Optional device filter (if not provided, returns global range)"),
    DB: Session = Depends(get_DB)
):
    """
    Get the available timestamp range (oldest and newest GPS data).
    
    **REPLACES**: WebSocket action 'get_timestamp_range'
    
    **Purpose**: 
    Used by frontend to:
    - Initialize date range picker with valid bounds
    - Validate user-selected date ranges
    - Display data availability to users
    
    **Parameters**:
    - `device_id` (optional): If provided, returns range for that device only.
                             If omitted, returns global range across all active devices.
    
    **Returns**:
```json
    {
        "oldest_timestamp": "2025-01-01T00:00:00Z",
        "newest_timestamp": "2025-01-12T10:30:00Z",
        "device_id": "DEVICE_001",
        "span_seconds": 950400
    }
```
    
    **HTTP Status Codes**:
    - 200: Success (range returned)
    - 404: No GPS data found for specified device/global
    - 500: Database error
    
    **Example Requests**:
    - Global range: `GET /gps_data/timestamps/range`
    - Device range: `GET /gps_data/timestamps/range?device_id=DEVICE_001`
    """
    try:
        if device_id:
            # Device-specific range
            oldest = gps_data_repo.get_oldest_gps_row_by_device(DB, device_id)
            newest = gps_data_repo.get_last_gps_row_by_device(DB, device_id)
            
            if not oldest or not newest:
                raise HTTPException(
                    status_code=404,
                    detail=f"No GPS data found for device '{device_id}'"
                )
        else:
            # Global range (all active devices)
            oldest = gps_data_repo.get_global_oldest_gps(DB)
            newest = gps_data_repo.get_global_newest_gps(DB)
            
            if not oldest or not newest:
                raise HTTPException(
                    status_code=404,
                    detail="No GPS data available in the system"
                )
        
        # Calculate span
        oldest_dt = datetime.fromisoformat(oldest["Timestamp"].replace("Z", "+00:00"))
        newest_dt = datetime.fromisoformat(newest["Timestamp"].replace("Z", "+00:00"))
        span_seconds = int((newest_dt - oldest_dt).total_seconds())
        
        return {
            "oldest_timestamp": oldest["Timestamp"],
            "newest_timestamp": newest["Timestamp"],
            "device_id": device_id,
            "span_seconds": span_seconds
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch timestamp range: {str(e)}"
        )


@router.get("/history", response_model=dict)
def get_gps_history(
    start: str = Query(..., description="Start timestamp in ISO 8601 format (UTC), e.g., '2025-01-12T08:00:00Z'"),
    end: str = Query(..., description="End timestamp in ISO 8601 format (UTC), e.g., '2025-01-12T10:00:00Z'"),
    device_id: Optional[str] = Query(None, description="Optional device filter (if not provided, returns all devices)"),
    format: str = Query("polyline", regex="^(polyline|raw)$", description="Response format: 'polyline' (default) or 'raw'"),
    DB: Session = Depends(get_DB)
):
    """
    Get historical GPS data within a time range.
    
    **REPLACES**: WebSocket action 'get_history'
    
    **Purpose**: 
    Used by frontend for:
    - Drawing historical routes on map
    - Exporting GPS data for reports
    - Analyzing vehicle movements
    
    **Parameters**:
    - `start`: Start of time range (inclusive, UTC)
    - `end`: End of time range (inclusive, UTC)
    - `device_id`: Optional filter (if omitted, returns all devices)
    - `format`: Response format
        - `polyline` (default): Optimized for map display (lat/lon only)
        - `raw`: Full GPS data (includes Altitude, Accuracy, etc.)
    
    **Returns (polyline format)**:
```json
    {
        "device_id": "DEVICE_001",
        "start": "2025-01-12T08:00:00Z",
        "end": "2025-01-12T10:00:00Z",
        "count": 240,
        "polyline": [
            {
                "lat": 10.9878,
                "lon": -74.7889,
                "timestamp": "2025-01-12T08:00:05Z",
                "geofence": {
                    "id": "WAREHOUSE_01",
                    "name": "Main Warehouse",
                    "event": "exit"
                }
            },
            ...
        ]
    }
```
    
    **HTTP Status Codes**:
    - 200: Success (history returned)
    - 400: Invalid timestamp format or start >= end
    - 404: No GPS data found in range
    - 500: Database error
    
    **Example Requests**:
    - Single device: `GET /gps_data/history?start=2025-01-12T08:00:00Z&end=2025-01-12T10:00:00Z&device_id=DEVICE_001`
    - All devices: `GET /gps_data/history?start=2025-01-12T08:00:00Z&end=2025-01-12T10:00:00Z`
    - Raw format: `GET /gps_data/history?start=...&end=...&format=raw`
    """
    try:
        # Parse timestamps
        try:
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
        except ValueError as ve:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timestamp format. Use ISO 8601 (e.g., '2025-01-12T08:00:00Z'). Error: {str(ve)}"
            )
        
        # Validate range
        if start_dt >= end_dt:
            raise HTTPException(
                status_code=400,
                detail="Parameter 'start' must be before 'end'"
            )
        
        # Query DB
        if device_id:
            history = gps_data_repo.get_gps_data_in_range_by_device(
                DB, device_id, start_dt, end_dt
            )
        else:
            history = gps_data_repo.get_gps_data_in_range(DB, start_dt, end_dt)
        
        if not history:
            raise HTTPException(
                status_code=404,
                detail=f"No GPS data found in the specified range{' for device ' + device_id if device_id else ''}"
            )
        
        # Format response
        if format == "polyline":
            polyline = []
            for p in history:
                point = {
                    "lat": p["Latitude"],
                    "lon": p["Longitude"],
                    "timestamp": p["Timestamp"]
                }
                
                # Include geofence if present
                if p.get("geofence"):
                    point["geofence"] = p["geofence"]
                
                polyline.append(point)
            
            return {
                "device_id": device_id,
                "start": start,
                "end": end,
                "count": len(polyline),
                "polyline": polyline
            }
        else:
            # Raw format (full GPS data)
            return {
                "device_id": device_id,
                "start": start,
                "end": end,
                "count": len(history),
                "history": history
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch GPS history: {str(e)}"
        )


@router.get("/trips", response_model=dict)
def get_trips_data(
    # Single trip query
    trip_id: Optional[str] = Query(None, description="Single trip ID (if provided, other filters are ignored)"),
    
    # Temporal filters
    start: Optional[str] = Query(None, description="Start timestamp (ISO 8601 UTC)"),
    end: Optional[str] = Query(None, description="End timestamp (ISO 8601 UTC)"),
    
    # Spatial filters
    center_lat: Optional[float] = Query(None, ge=-90, le=90, description="Center latitude (decimal degrees)"),
    center_lon: Optional[float] = Query(None, ge=-180, le=180, description="Center longitude (decimal degrees)"),
    radius_meters: Optional[float] = Query(None, gt=0, le=100000, description="Search radius in meters (max 100km)"),
    
    # Device filter
    device_id: Optional[str] = Query(None, description="Optional device filter"),
    
    DB: Session = Depends(get_DB)
):
    """
    Get trips with optional temporal/spatial filters.
    
    **REPLACES**: WebSocket action 'get_trips'
    
    **Purpose**: 
    Used by frontend for:
    - Analyzing vehicle routes and stops
    - Generating trip reports
    - Searching trips near locations (geofences)
    
    **Query Modes**:
    
    1. **Single Trip** (highest priority):
       - `?trip_id=TRIP_20250112_DEVICE001_083000`
    
    2. **Temporal Query**:
       - `?start=2025-01-12T00:00:00Z&end=2025-01-12T23:59:59Z`
       - Returns trips that overlap with the time range
    
    3. **Spatial Query**:
       - `?center_lat=10.9878&center_lon=-74.7889&radius_meters=500`
       - Returns trips that passed within radius of center point
    
    4. **Hybrid Query** (temporal AND spatial):
       - `?start=...&end=...&center_lat=...&center_lon=...&radius_meters=...`
       - Returns trips matching BOTH criteria
    
    5. **Device Filter** (can be combined with any mode):
       - Add `&device_id=DEVICE_001` to any query
    
    **Returns**:
```json
    {
        "trips": [
            {
                "trip_id": "TRIP_20250112_DEVICE001_083000",
                "device_id": "DEVICE_001",
                "type": "movement",
                "status": "closed",
                "start_time": "2025-01-12T08:30:00Z",
                "end_time": "2025-01-12T09:00:00Z",
                "metrics": {
                    "distance_m": 5420.5,
                    "duration_s": 1800.0,
                    "avg_speed_kmh": 10.84,
                    "point_count": 360
                },
                "route": [
                    {
                        "timestamp": "2025-01-12T08:30:05Z",
                        "gps": {"lat": 10.9878, "lon": -74.7889},
                        "geofence": {...},
                        "accel": {...}
                    },
                    ...
                ]
            }
        ],
        "summary": {
            "total_trips": 5,
            "total_points": 1800,
            "devices": ["DEVICE_001", "DEVICE_002"]
        }
    }
```
    
    **HTTP Status Codes**:
    - 200: Success (trips returned, may be empty array)
    - 400: Invalid parameters (bad timestamp, invalid coordinates, missing required params)
    - 500: Database error
    
    **Example Requests**:
    - Single trip: `GET /gps_data/trips?trip_id=TRIP_20250112_...`
    - Today's trips: `GET /gps_data/trips?start=2025-01-12T00:00:00Z&end=2025-01-12T23:59:59Z`
    - Near warehouse: `GET /gps_data/trips?center_lat=10.9878&center_lon=-74.7889&radius_meters=500`
    - Device trips: `GET /gps_data/trips?start=...&end=...&device_id=DEVICE_001`
    """
    from src.Services import request_handlers
    
    try:
        # Build params dict (same format as WebSocket handler for reusability)
        params = {}
        
        if trip_id:
            params['trip_id'] = trip_id
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        if device_id:
            params['device_id'] = device_id
        
        # Spatial parameters (must be provided together)
        if center_lat is not None and center_lon is not None:
            params['center'] = {'lat': center_lat, 'lon': center_lon}
        elif center_lat is not None or center_lon is not None:
            raise HTTPException(
                status_code=400,
                detail="Spatial query requires both 'center_lat' and 'center_lon'"
            )
        
        if radius_meters is not None:
            if 'center' not in params:
                raise HTTPException(
                    status_code=400,
                    detail="Parameter 'radius_meters' requires 'center_lat' and 'center_lon'"
                )
            params['radius_meters'] = radius_meters
        
        # Reuse existing handler logic (DRY principle)
        # The handler contains complex logic for temporal/spatial/hybrid queries
        result = request_handlers.handle_get_trips(params, "http_request")
        
        # Check if handler returned an error
        if result['status'] == 'error':
            raise HTTPException(
                status_code=400,
                detail=result['data'].get('error', 'Unknown error')
            )
        
        # Return the data payload (trips + summary)
        return result['data']
    
    except HTTPException:
        raise
    except ValueError as ve:
        # Validation errors from handler
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch trips: {str(e)}"
        )


# ==========================================================
# ✅ STANDARD CRUD ROUTES (Variable path parameters - LAST)
# ==========================================================
# These endpoints use path parameters and MUST be defined AFTER
# all specific routes to prevent routing conflicts.
#
# FastAPI matches routes in order: /{gps_data_id} will match ANY string
# including "history", "trips", etc. if defined before those routes.
# ==========================================================

@router.get("/{gps_data_id}", response_model=gps_data_schema.GpsData_get)
def read_gps_data_by_id(gps_data_id: int, DB: Session = Depends(get_DB)):
    """
    Get a specific GPS record by its internal database ID.
    
    Useful for debugging or direct record access.
    
    Args:
        gps_data_id: Internal database ID of the GPS record
        
    Returns:
        GPS record with the specified ID
        
    Example:
        GET /gps_data/12345
    
    Raises:
        404: GPS data not found
    """
    db_gps_data = gps_data_repo.get_gps_data_by_id(DB, gps_data_id=gps_data_id)
    
    if db_gps_data is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    
    return db_gps_data


@router.post("/post", response_model=gps_data_schema.GpsData_get)
def create_gps_data(
    gps_data: gps_data_schema.GpsData_create, 
    DB: Session = Depends(get_DB)
):
    """
    Create a new GPS record manually.
    
    Note: In production, GPS data is typically inserted via UDP service.
    This endpoint is useful for testing or manual data entry.
    
    Args:
        gps_data: GPS data payload (DeviceID, Lat, Lon, Timestamp, etc.)
        
    Returns:
        Created GPS record with assigned ID
        
    Example:
        POST /gps_data/post
        Body: {
            "DeviceID": "TRUCK-001",
            "Latitude": 10.9878,
            "Longitude": -74.7889,
            "Altitude": 12.5,
            "Accuracy": 8.0,
            "Timestamp": "2025-10-21T14:30:00Z"
        }
    """
    return gps_data_repo.created_gps_data(DB, gps_data)


@router.patch("/{gps_data_id}", response_model=gps_data_schema.GpsData_get)
def update_gps_data(
    gps_data_id: int, 
    gps_data: gps_data_schema.GpsData_update, 
    DB: Session = Depends(get_DB)
):
    """
    Update an existing GPS record.
    
    Args:
        gps_data_id: Internal database ID of the GPS record to update
        gps_data: Fields to update (all optional)
        
    Returns:
        Updated GPS record
        
    Example:
        PATCH /gps_data/12345
        Body: {"Accuracy": 5.0}
    
    Raises:
        404: GPS data not found
    """
    updated = gps_data_repo.update_gps_data(DB, gps_data_id, gps_data)
    
    if updated is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    
    return updated


@router.delete("/{gps_data_id}", response_model=gps_data_schema.GpsData_delete)
def delete_gps_data(gps_data_id: int, DB: Session = Depends(get_DB)):
    """
    Delete a GPS record by its internal database ID.
    
    Warning: This permanently removes the record from the database.
    
    Args:
        gps_data_id: Internal database ID of the GPS record to delete
        
    Returns:
        Deleted record ID confirmation
        
    Example:
        DELETE /gps_data/12345
    
    Raises:
        404: GPS data not found
    """
    deleted_id = gps_data_repo.delete_gps_data(DB, gps_data_id)
    
    if deleted_id is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    
    return {"id": deleted_id}