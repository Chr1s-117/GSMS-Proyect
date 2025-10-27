# src/Services/gps_serialization.py

"""
GPS Data Serialization Service

This module provides utilities to convert SQLAlchemy GPS_data ORM objects
to JSON-serializable dictionaries suitable for API responses and WebSocket broadcasts.

Key Features:
- Pydantic schema validation
- UTC ISO 8601 timestamp formatting with 'Z' suffix
- Geofence information restructuring for frontend consumption
- Removal of internal database fields
- Null handling and filtering

Serialization Format:
    Input (ORM object):
        GPS_data(
            id=12345,
            DeviceID="TRUCK-001",
            Latitude=10.9878,
            Longitude=-74.7889,
            Timestamp=datetime(2025, 1, 27, 6, 4, 54, tzinfo=UTC),
            CurrentGeofenceID="warehouse-001",
            CurrentGeofenceName="Main Warehouse",
            GeofenceEventType="entry"
        )
    
    Output (dict):
        {
            "DeviceID": "TRUCK-001",
            "Latitude": 10.9878,
            "Longitude": -74.7889,
            "Timestamp": "2025-01-27T06:04:54Z",
            "geofence": {
                "id": "warehouse-001",
                "name": "Main Warehouse",
                "event": "entry"
            }
        }

Usage:
    from src.Services.gps_serialization import serialize_gps_row, serialize_many
    
    # Single GPS record
    gps_dict = serialize_gps_row(gps_record, include_id=False)
    
    # Multiple GPS records
    gps_list = serialize_many(gps_records, include_id=False)
"""

from datetime import datetime, timezone
from typing import Any, Optional, List
from src.Schemas.gps_data import GpsData_get
from src.Models.gps_data import GPS_data


# ==========================================================
# 📌 Single GPS Record Serialization
# ==========================================================

def serialize_gps_row(
    row: Optional[GPS_data], 
    include_id: bool = False
) -> Optional[dict[str, Any]]:
    """
    Convert a single GPS_data ORM object to a JSON-serializable dictionary.
    
    This function:
    1. Validates the ORM object using Pydantic schema
    2. Converts to dictionary
    3. Normalizes timestamp to UTC ISO 8601 format with 'Z' suffix
    4. Restructures geofence information for frontend consumption
    5. Removes internal database fields
    
    Args:
        row: SQLAlchemy GPS_data object or None
        include_id: If True, includes internal database ID in output (default: False)
        
    Returns:
        JSON-serializable dictionary or None if input is None
        
    Example:
        # Without ID (for API responses)
        gps_dict = serialize_gps_row(gps_record)
        # {
        #     "DeviceID": "TRUCK-001",
        #     "Latitude": 10.9878,
        #     "Longitude": -74.7889,
        #     "Timestamp": "2025-01-27T06:04:54Z",
        #     "geofence": {"id": "warehouse-001", "name": "Main Warehouse", "event": "entry"}
        # }
        
        # With ID (for internal use)
        gps_dict = serialize_gps_row(gps_record, include_id=True)
        # Includes: "id": 12345
    
    Timestamp Format:
        - Input: datetime object with timezone info
        - Output: "2025-01-27T06:04:54Z" (UTC ISO 8601 with 'Z' suffix)
        - Always converted to UTC regardless of input timezone
    
    Geofence Restructuring:
        Database fields (internal):
            CurrentGeofenceID: "warehouse-001"
            CurrentGeofenceName: "Main Warehouse"
            GeofenceEventType: "entry"
        
        Output structure (frontend-friendly):
            geofence: {
                "id": "warehouse-001",
                "name": "Main Warehouse",
                "event": "entry"
            }
        
        If outside all geofences:
            geofence: null
    
    Performance:
        - Pydantic validation: <1ms per record
        - Timestamp conversion: <0.1ms
        - Total: <2ms per record typical
    """
    if row is None:
        return None

    # Determine which fields to exclude
    exclude_fields = set() if include_id else {"id"}
    
    # ORM object → Pydantic validation → dict
    data = GpsData_get.model_validate(row).model_dump(exclude=exclude_fields)

    # ========================================
    # Normalize timestamp to UTC ISO 8601 with 'Z'
    # ========================================
    ts = data.get("Timestamp")
    if isinstance(ts, datetime):
        # Convert to UTC and format with 'Z' suffix (standard for UTC)
        data["Timestamp"] = ts.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        data["Timestamp"] = None

    # ========================================
    # Restructure geofence info for frontend
    # ========================================
    geofence_id = data.get("CurrentGeofenceID")
    geofence_name = data.get("CurrentGeofenceName")
    event_type = data.get("GeofenceEventType")

    # Create nested geofence object if:
    # - Device is inside a geofence (geofence_id present), OR
    # - Device just exited a geofence (event_type == 'exit')
    if geofence_id or event_type == 'exit':
        data["geofence"] = {
            "id": geofence_id,      # String or None
            "name": geofence_name,  # String or None
            "event": event_type     # "entry" | "exit" | "inside" | None
        }
    else:
        # Device is outside all geofences and has been for some time
        data["geofence"] = None

    # Remove internal database fields from payload
    # (they're now restructured in the nested 'geofence' object)
    data.pop("CurrentGeofenceID", None)
    data.pop("CurrentGeofenceName", None)
    data.pop("GeofenceEventType", None)

    return data


# ==========================================================
# 📌 Multiple GPS Records Serialization
# ==========================================================

def serialize_many(
    rows: List[GPS_data], 
    include_id: bool = False
) -> List[dict[str, Any]]:
    """
    Convert a list of GPS_data ORM objects to a list of JSON-serializable dictionaries.
    
    This is a batch version of serialize_gps_row that:
    1. Applies serialize_gps_row to each element
    2. Automatically filters out None values
    3. Returns a clean list ready for JSON serialization
    
    Args:
        rows: List of SQLAlchemy GPS_data objects
        include_id: If True, includes internal database IDs (default: False)
        
    Returns:
        List of JSON-serializable dictionaries (nulls filtered out)
        
    Example:
        gps_list = serialize_many(gps_records)
        # [
        #     {"DeviceID": "TRUCK-001", "Latitude": 10.9878, ...},
        #     {"DeviceID": "TRUCK-001", "Latitude": 10.9880, ...},
        #     ...
        # ]
    
    Use Cases:
        - Historical route queries (get_gps_data_in_range_by_device)
        - Multi-device latest positions (get_last_gps_all_devices)
        - Time-range analytics
        - API list endpoints
        - WebSocket batch broadcasts
    
    Null Handling:
        - If a row is None, it's silently skipped
        - If serialize_gps_row returns None, it's filtered out
        - Result is always a clean list with no nulls
    
    Performance:
        - Uses list comprehension with walrus operator for efficiency
        - Typical: <5ms for 100 records
        - Memory efficient (no intermediate lists)
    
    Example with filtering:
        rows = [gps1, None, gps2, gps3]
        result = serialize_many(rows)
        # Result contains only gps1, gps2, gps3 (None filtered out)
    """
    return [
        serialized 
        for row in rows 
        if (serialized := serialize_gps_row(row, include_id=include_id)) is not None
    ]