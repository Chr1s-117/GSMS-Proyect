# ==========================================================
# Archivo: src/Services/request_handlers.py
# Descripción:
#   WebSocket/HTTP request handlers for GPS/RouteManager
#   Pure functions without global state, with comprehensive error handling
#   
# Architecture:
#   - Each handler is a pure function that receives params and returns response
#   - All database operations use context managers (with SessionLocal)
#   - Standardized response format via build_response()
#   - Type-safe with type hints
#   - Comprehensive error handling and logging
# ==========================================================

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from src.DB.session import SessionLocal
from src.Repositories.gps_data import (
    get_all_devices,
    get_last_gps_all_devices,
    get_gps_data_in_range_by_device,
    get_oldest_gps_row_by_device,
    get_last_gps_row_by_device,
    get_global_oldest_gps,
    get_global_newest_gps,
    get_gps_data_in_range
)
from src.Services.gps_broadcaster import add_gps


# ==========================================================
# Global Utility Function
# ==========================================================

def build_response(
    action: str, 
    request_id: str, 
    data: Any, 
    status: str = "success"
) -> Dict[str, Any]:
    """
    Build standardized response structure for WebSocket/HTTP.
    
    All handlers must return responses in this format for consistency
    across the application and to enable proper client-side handling.
    
    Args:
        action: Action identifier (e.g., "ping", "get_devices", "get_history")
        request_id: Unique request identifier from client (for correlation)
        data: Response payload (any JSON-serializable data)
        status: Response status - "success" | "error" (default: "success")
        
    Returns:
        Standardized response dictionary:
        {
            "action": "get_devices",
            "request_id": "req-12345",
            "status": "success",
            "data": {...}
        }
        
    Example:
        return build_response("ping", "req-001", "pong")
        # {"action": "ping", "request_id": "req-001", "status": "success", "data": "pong"}
        
        return build_response("get_devices", "req-002", {"error": "DB error"}, status="error")
        # {"action": "get_devices", "request_id": "req-002", "status": "error", "data": {"error": "..."}}
    """
    return {
        "action": action,
        "request_id": request_id,
        "status": status,
        "data": data
    }


# ==========================================================
# Simple Handlers (No Database)
# ==========================================================

def handle_ping(params: Dict[str, Any], request_id: str) -> dict:
    """
    Health check handler.
    
    Simple ping/pong for WebSocket connection verification.
    No database access, always succeeds unless catastrophic error.
    
    Args:
        params: Request parameters (unused for ping)
        request_id: Unique request identifier
        
    Returns:
        Standardized response with "pong" data
        
    Example request:
        {"action": "ping", "request_id": "req-001", "params": {}}
        
    Example response:
        {"action": "ping", "request_id": "req-001", "status": "success", "data": "pong"}
    """
    try:
        return build_response("ping", request_id, "pong")
    except Exception as e:
        print(f"[HANDLER] Unexpected error in handle_ping: {e}")
        return build_response("ping", request_id, {"error": str(e)}, status="error")


# ==========================================================
# Database Query Handlers (Simple)
# ==========================================================

def handle_get_devices(params: Dict[str, Any], request_id: str) -> dict:
    """
    Get list of all registered devices.
    
    Queries the 'devices' table (not GPS table) to return all registered
    device identifiers. Useful for populating device selection dropdowns
    in frontend.
    
    Args:
        params: Request parameters (unused)
        request_id: Unique request identifier
        
    Returns:
        Response with device list and count:
        {
            "devices": ["TRUCK-001", "TRUCK-002", ...],
            "count": 25
        }
        
    Example request:
        {"action": "get_devices", "request_id": "req-002", "params": {}}
        
    Example response:
        {
            "action": "get_devices",
            "request_id": "req-002",
            "status": "success",
            "data": {
                "devices": ["TRUCK-001", "TRUCK-002"],
                "count": 2
            }
        }
    """
    try:
        with SessionLocal() as db:
            devices = get_all_devices(db)
            data = {
                "devices": devices, 
                "count": len(devices)
            }
        return build_response("get_devices", request_id, data)
    
    except Exception as e:
        print(f"[HANDLER] Error in handle_get_devices: {e}")
        return build_response(
            "get_devices", 
            request_id, 
            {"error": str(e)}, 
            status="error"
        )


def handle_get_last_positions(params: Dict[str, Any], request_id: str) -> dict:
    """
    Get latest GPS position for all devices and broadcast via WebSocket.
    
    This handler:
    1. Queries the latest GPS record for each registered device
    2. Broadcasts each position via GPS WebSocket channel (add_gps)
    3. Returns confirmation with count
    
    Used for:
    - Initial map load (show all device positions)
    - Refresh all positions button
    - Recovery after WebSocket reconnection
    
    Args:
        params: Request parameters
            - subscribe: bool (optional) - Enable continuous monitoring
        request_id: Unique request identifier
        
    Returns:
        Response with confirmation message and device count:
        {
            "message": "Last positions sent",
            "count": 25
        }
        
    Example request:
        {"action": "get_last_positions", "request_id": "req-003", "params": {}}
        
    Example response:
        {
            "action": "get_last_positions",
            "request_id": "req-003",
            "status": "success",
            "data": {
                "message": "Last positions sent",
                "count": 25
            }
        }
        
    Side effects:
        - Broadcasts GPS data via add_gps() for each device
        - If params["subscribe"] is True, activates continuous monitoring (handled in request_ws.py)
    """
    try:
        with SessionLocal() as db:
            last_positions = get_last_gps_all_devices(db)
            count = 0
            
            # Broadcast each device's latest position
            for device_id, gps_data in last_positions.items():
                add_gps(gps_data)
                count += 1
        
        return build_response(
            "get_last_positions", 
            request_id, 
            {
                "message": "Last positions sent", 
                "count": count
            }
        )
    
    except Exception as e:
        print(f"[HANDLER] Error in handle_get_last_positions: {e}")
        return build_response(
            "get_last_positions", 
            request_id, 
            {"error": str(e)}, 
            status="error"
        )


# ==========================================================
# Timestamp Range Handler
# ==========================================================

def handle_get_timestamp_range(params: Dict[str, Any], request_id: str) -> dict:
    """
    Get available timestamp range (oldest and newest GPS records).
    
    This handler supports two modes:
    
    1. Device-specific mode (device_id provided):
       - Returns timestamp range for specific device
       - Useful for device history timeline
    
    2. Global mode (no device_id):
       - Returns timestamp range across ALL active devices
       - Useful for global timeline/calendar controls
    
    Args:
        params: Request parameters
            - device_id: str (optional) - Specific device to query
        request_id: Unique request identifier
        
    Returns:
        Response with timestamp range and span:
        {
            "oldest_timestamp": "2025-01-01T00:00:00Z",
            "newest_timestamp": "2025-10-22T09:53:12Z",
            "device_id": "TRUCK-001" or null,
            "span_seconds": 25920000,
            "span_days": 300
        }
        
    Example request (device-specific):
        {
            "action": "get_timestamp_range",
            "request_id": "req-004",
            "params": {"device_id": "TRUCK-001"}
        }
        
    Example request (global):
        {
            "action": "get_timestamp_range",
            "request_id": "req-005",
            "params": {}
        }
        
    Example response:
        {
            "action": "get_timestamp_range",
            "request_id": "req-004",
            "status": "success",
            "data": {
                "oldest_timestamp": "2025-09-01T08:00:00Z",
                "newest_timestamp": "2025-10-22T09:53:12Z",
                "device_id": "TRUCK-001",
                "span_seconds": 4435392,
                "span_days": 51
            }
        }
    """
    try:
        device_id = params.get("device_id")
        
        with SessionLocal() as db:
            if device_id:
                # Device-specific range
                oldest = get_oldest_gps_row_by_device(db, device_id)
                newest = get_last_gps_row_by_device(db, device_id)
                
                if not oldest or not newest:
                    return build_response(
                        "get_timestamp_range",
                        request_id,
                        {"error": f"No GPS data for device '{device_id}'"},
                        status="error"
                    )
            else:
                # Global range (all active devices)
                oldest = get_global_oldest_gps(db)
                newest = get_global_newest_gps(db)
                
                if not oldest or not newest:
                    return build_response(
                        "get_timestamp_range",
                        request_id,
                        {"error": "No GPS data available"},
                        status="error"
                    )
            
            # Calculate time span
            oldest_dt = datetime.fromisoformat(oldest["Timestamp"].replace("Z", "+00:00"))
            newest_dt = datetime.fromisoformat(newest["Timestamp"].replace("Z", "+00:00"))
            span_seconds = (newest_dt - oldest_dt).total_seconds()
            span_days = span_seconds / 86400  # Convert to days
            
            data = {
                "oldest_timestamp": oldest["Timestamp"],
                "newest_timestamp": newest["Timestamp"],
                "device_id": device_id,
                "span_seconds": int(span_seconds),
                "span_days": round(span_days, 1)
            }
            
        return build_response("get_timestamp_range", request_id, data)
    
    except Exception as e:
        print(f"[HANDLER] Error in handle_get_timestamp_range: {e}")
        return build_response(
            "get_timestamp_range",
            request_id,
            {"error": str(e)},
            status="error"
        )


# ==========================================================
# Complex Handler (History with Geofence Data)
# ==========================================================

def handle_get_history(params: Dict[str, Any], request_id: str) -> dict:
    """
    Get historical GPS data within a time range with geofence information.
    
    This is the most complex handler, supporting multiple modes:
    
    1. Device-specific history (device_id provided):
       - Returns GPS points for specific device
       - Two formats: "polyline" (optimized for map) or "full" (complete data)
    
    2. Global history (no device_id, LEGACY):
       - Returns GPS from ALL devices
       - Use with caution (can be large dataset)
    
    Format types:
    - "polyline": Optimized for map rendering (lat/lon/timestamp/geofence)
    - "full": Complete GPS data with all fields
    
    Args:
        params: Request parameters
            - start: str (required) - Start timestamp in ISO-8601 UTC
            - end: str (required) - End timestamp in ISO-8601 UTC
            - device_id: str (optional) - Specific device to query
            - format: str (optional) - "polyline" | "full" (default: "polyline")
        request_id: Unique request identifier
        
    Returns:
        Response with GPS history in requested format:
        
        Polyline format:
        {
            "device_id": "TRUCK-001",
            "start": "2025-10-22T00:00:00Z",
            "end": "2025-10-22T23:59:59Z",
            "count": 1500,
            "polyline": [
                {
                    "lat": 10.9878,
                    "lon": -74.7889,
                    "timestamp": "2025-10-22T09:15:30Z",
                    "geofence": {
                        "id": "warehouse-001",
                        "name": "Main Warehouse",
                        "event": "entry"
                    }
                },
                ...
            ]
        }
        
        Full format:
        {
            "device_id": "TRUCK-001",
            "start": "2025-10-22T00:00:00Z",
            "end": "2025-10-22T23:59:59Z",
            "count": 1500,
            "history": [
                {
                    "id": 12345,
                    "DeviceID": "TRUCK-001",
                    "Latitude": 10.9878,
                    "Longitude": -74.7889,
                    "Altitude": 12.5,
                    "Accuracy": 8.0,
                    "Timestamp": "2025-10-22T09:15:30Z",
                    "geofence": {...}
                },
                ...
            ]
        }
        
    Example request:
        {
            "action": "get_history",
            "request_id": "req-006",
            "params": {
                "device_id": "TRUCK-001",
                "start": "2025-10-22T00:00:00Z",
                "end": "2025-10-22T23:59:59Z",
                "format": "polyline"
            }
        }
    """
    try:
        # Extract and validate parameters
        start_str = params.get("start")
        end_str = params.get("end")
        device_id = params.get("device_id")
        format_type = params.get("format", "polyline")

        if not start_str or not end_str:
            raise ValueError("Missing required 'start' or 'end' parameter")

        # Parse timestamps
        start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))

        with SessionLocal() as db:
            if device_id:
                # Device-specific history
                history = get_gps_data_in_range_by_device(db, device_id, start_dt, end_dt, include_id=True)
                
                if format_type == "polyline":
                    # Optimized format for map rendering
                    polyline = []
                    for p in history:
                        # Skip invalid coordinates
                        if p.get("Latitude") is None or p.get("Longitude") is None:
                            continue
                        
                        point = {
                            "lat": p["Latitude"],
                            "lon": p["Longitude"],
                            "timestamp": p["Timestamp"]
                        }
                        
                        # Include geofence data if available
                        if p.get("geofence"):
                            point["geofence"] = p["geofence"]
                        
                        polyline.append(point)
                    
                    data = {
                        "device_id": device_id,
                        "start": start_str,
                        "end": end_str,
                        "count": len(polyline),
                        "polyline": polyline
                    }
                else:
                    # Full format with all GPS fields
                    data = {
                        "device_id": device_id,
                        "start": start_str,
                        "end": end_str,
                        "count": len(history),
                        "history": history
                    }
            else:
                # Global history (LEGACY - all devices)
                print(f"[HANDLER] WARNING: Global history query (all devices) from request {request_id}")
                history = get_gps_data_in_range(db, start_dt, end_dt, include_id=True)
                data = {
                    "start": start_str,
                    "end": end_str,
                    "count": len(history),
                    "history": history
                }
        
        return build_response("get_history", request_id, data)
    
    except ValueError as ve:
        print(f"[HANDLER] Validation error in handle_get_history: {ve}")
        return build_response(
            "get_history",
            request_id,
            {"error": str(ve)},
            status="error"
        )
    
    except Exception as e:
        print(f"[HANDLER] Error in handle_get_history: {e}")
        return build_response(
            "get_history",
            request_id,
            {"error": str(e)},
            status="error"
        )