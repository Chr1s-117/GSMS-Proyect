# src/Controller/Routes/gps_datas.py

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.Controller.deps import get_DB
from src.Repositories import gps_data as gps_data_repo
from src.Schemas import gps_data as gps_data_schema

router = APIRouter()

# ==========================================================
# ✅ SPECIAL GET ROUTES (Cleaned & Updated)
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
# ✅ STANDARD CRUD ROUTES
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