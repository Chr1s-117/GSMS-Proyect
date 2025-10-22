# src/Services/gps_serialization.py

from datetime import datetime, timezone
from typing import Any, Optional
from src.Schemas.gps_data import GpsData_get
from src.Models.gps_data import GPS_data


def serialize_gps_row(row: Optional[GPS_data], include_id: bool = False) -> Optional[dict[str, Any]]:
    """
    Convert a GPS_data SQLAlchemy row into a JSON-serializable dictionary.
    
    This function performs the following transformations:
    1. Validates ORM data using Pydantic schema
    2. Normalizes timestamp to UTC ISO-8601 format with 'Z' suffix
    3. Restructures geofence fields into a nested 'geofence' object for frontend
    4. Removes internal database fields based on include_id parameter
    
    Args:
        row: GPS_data ORM object from database query (can be None)
        include_id: If True, includes the internal 'id' field in output
        
    Returns:
        JSON-serializable dict with GPS data, or None if input row is None
        
    Example output (without geofence):
        {
            "DeviceID": "TRUCK-001",
            "Latitude": 10.9878,
            "Longitude": -74.7889,
            "Altitude": 12.5,
            "Accuracy": 8.0,
            "Timestamp": "2025-10-22T09:34:28Z",
            "geofence": null
        }
    
    Example output (with geofence):
        {
            "DeviceID": "TRUCK-001",
            "Latitude": 10.9878,
            "Longitude": -74.7889,
            "Altitude": 12.5,
            "Accuracy": 8.0,
            "Timestamp": "2025-10-22T09:34:28Z",
            "geofence": {
                "id": "warehouse-001",
                "name": "Main Warehouse",
                "event": "entry"
            }
        }
    
    Example output (with id included):
        {
            "id": 12345,
            "DeviceID": "TRUCK-001",
            ...
        }
    """
    if row is None:
        return None

    exclude_fields = set() if include_id else {"id"}
    
    # Convert ORM object to dict using Pydantic validation
    data = GpsData_get.model_validate(row).model_dump(exclude=exclude_fields)

    # ========================================
    # ✅ NORMALIZE TIMESTAMP TO UTC ISO-8601
    # ========================================
    ts = data.get("Timestamp")
    if isinstance(ts, datetime):
        # Ensure UTC timezone and format with 'Z' suffix
        data["Timestamp"] = ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        data["Timestamp"] = None

    # ========================================
    # ✅ FORMAT GEOFENCE DATA FOR FRONTEND
    # ========================================
    geofence_id = data.get("CurrentGeofenceID")
    geofence_name = data.get("CurrentGeofenceName")
    event_type = data.get("GeofenceEventType")

    # Create nested geofence object if geofence data exists
    # Special case: 'exit' events should always include geofence info (last known geofence)
    if geofence_id or event_type == 'exit':
        data["geofence"] = {
            "id": geofence_id,
            "name": geofence_name,
            "event": event_type
        }
    else:
        # GPS point is outside all geofences
        data["geofence"] = None

    # Remove internal database fields from final payload
    data.pop("CurrentGeofenceID", None)
    data.pop("CurrentGeofenceName", None)
    data.pop("GeofenceEventType", None)

    return data


def serialize_many(rows: list[GPS_data], include_id: bool = False) -> list[dict[str, Any]]:
    """
    Convert a list of GPS_data rows into a list of JSON-serializable dictionaries.
    
    This is a batch version of serialize_gps_row() with automatic filtering
    of null or invalid rows.
    
    Args:
        rows: List of GPS_data ORM objects from database query
        include_id: If True, includes the internal 'id' field in each dict
        
    Returns:
        List of JSON-serializable dicts (empty list if no valid rows)
        
    Example usage:
        # Get GPS history from repository
        gps_rows = db.query(GPS_data).filter(...).all()
        
        # Serialize for API response
        serialized = serialize_many(gps_rows, include_id=True)
        
        # Returns:
        # [
        #     {"id": 1, "DeviceID": "TRUCK-001", "Latitude": 10.9878, ...},
        #     {"id": 2, "DeviceID": "TRUCK-001", "Latitude": 10.9880, ...},
        #     ...
        # ]
    
    Performance note:
        - Uses walrus operator := for efficient filtering
        - Automatically skips None results from serialize_gps_row()
        - Preserves chronological order from input list
    """
    return [
        serialized 
        for row in rows 
        if (serialized := serialize_gps_row(row, include_id=include_id)) is not None
    ]


def deserialize_timestamp(timestamp_str: str) -> datetime:
    """
    Convert ISO-8601 timestamp string to timezone-aware datetime object.
    
    Supports multiple formats:
    - "2025-10-22T09:34:28Z" (with Z suffix)
    - "2025-10-22T09:34:28+00:00" (with explicit timezone)
    - "2025-10-22T09:34:28" (naive, assumes UTC)
    
    Args:
        timestamp_str: ISO-8601 formatted timestamp string
        
    Returns:
        Timezone-aware datetime object in UTC
        
    Raises:
        ValueError: If timestamp format is invalid
        
    Example:
        ts = deserialize_timestamp("2025-10-22T09:34:28Z")
        # Returns: datetime(2025, 10, 22, 9, 34, 28, tzinfo=timezone.utc)
    """
    # Remove 'Z' suffix and replace with +00:00 for parsing
    timestamp_str = timestamp_str.replace("Z", "+00:00")
    
    try:
        dt = datetime.fromisoformat(timestamp_str)
        
        # Ensure timezone-aware (assume UTC if naive)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        return dt
    except ValueError as e:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}") from e


def format_geofence_event(
    geofence_id: Optional[str],
    geofence_name: Optional[str],
    event_type: Optional[str]
) -> Optional[dict[str, Any]]:
    """
    Format geofence data into a consistent structure for API responses.
    
    This is a helper function used internally by serialize_gps_row().
    Can also be used standalone when building custom responses.
    
    Args:
        geofence_id: Geofence identifier (can be None)
        geofence_name: Human-readable geofence name (can be None)
        event_type: Event type ('entry', 'exit', 'inside', or None)
        
    Returns:
        Formatted geofence dict, or None if no geofence data
        
    Example:
        # GPS inside geofence
        result = format_geofence_event("warehouse-001", "Main Warehouse", "entry")
        # Returns: {"id": "warehouse-001", "name": "Main Warehouse", "event": "entry"}
        
        # GPS outside all geofences
        result = format_geofence_event(None, None, None)
        # Returns: None
        
        # GPS exiting geofence (special case: includes last known geofence)
        result = format_geofence_event("warehouse-001", "Main Warehouse", "exit")
        # Returns: {"id": "warehouse-001", "name": "Main Warehouse", "event": "exit"}
    """
    if geofence_id or event_type == 'exit':
        return {
            "id": geofence_id,
            "name": geofence_name,
            "event": event_type
        }
    return None