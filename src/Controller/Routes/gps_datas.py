# src/Controller/Routes/gps_datas.py

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.Controller.deps import get_DB
from src.Repositories import gps_data as gps_data_repo
from src.Schemas import gps_data as gps_data_schema

# -------------------------------------------------------------------
# GPS Data API Router
# -------------------------------------------------------------------
# This module defines all CRUD endpoints for GPS data.
# Each endpoint is fully typed, returns proper response models,
# and uses dependency injection for the database session.
# All exceptions are handled to return standard HTTP responses.
# -------------------------------------------------------------------

router = APIRouter()

# ---------- SPECIAL GET ROUTES ----------

@router.get("/last", response_model=gps_data_schema.GpsData_get)
def get_last_gps_row(DB: Session = Depends(get_DB)):
    """
    Retrieve the most recent GPS data record from the database.

    Args:
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Raises:
        HTTPException(404): If no GPS data exists in the database.

    Returns:
        GpsData_get: The most recent GPS record, serialized using Pydantic.
    """
    last_row = gps_data_repo.get_last_gps_row(DB, include_id=True)  
    if last_row is None:
        raise HTTPException(status_code=404, detail="No GPS data found")
    return last_row

@router.get("/oldest", response_model=gps_data_schema.GpsData_get)
def get_oldest_gps_row(DB: Session = Depends(get_DB)):
    """
    Retrieve the oldest GPS data record from the database.

    Args:
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Raises:
        HTTPException(404): If no GPS data exists in the database.

    Returns:
        GpsData_get: The oldest GPS record, serialized using Pydantic.
    """
    oldest_row = gps_data_repo.get_oldest_gps_row(DB, include_id=True)  
    if oldest_row is None:
        raise HTTPException(status_code=404, detail="No GPS data found")
    return oldest_row

@router.get("/range", response_model=List[gps_data_schema.GpsData_get])
def get_gps_data_range(
    start: datetime = Query(..., description="Start timestamp in ISO-8601 UTC"),
    end: datetime = Query(..., description="End timestamp in ISO-8601 UTC"),
    DB: Session = Depends(get_DB)
):
    """
    Retrieve all GPS data records within a specified timestamp range.

    Args:
        start (datetime): Start timestamp in ISO-8601 UTC format.
        end (datetime): End timestamp in ISO-8601 UTC format.
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Raises:
        HTTPException(404): If no GPS data exists within the given range.

    Returns:
        List[GpsData_get]: A list of GPS records within the range, serialized using Pydantic.
    """
    data = gps_data_repo.get_gps_data_in_range(DB, start, end, include_id=True)
    if not data:
        raise HTTPException(status_code=404, detail="No GPS data found in range")
    return data

# ---------- STANDARD CRUD ROUTES ----------

@router.get("/", response_model=List[gps_data_schema.GpsData_get])
def read_gps_data(DB: Session = Depends(get_DB)):
    """
    Retrieve all GPS data records from the database.

    Args:
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Returns:
        List[GpsData_get]: A list of all GPS records, serialized using Pydantic.
    """
    return gps_data_repo.get_gps_data(DB)

@router.get("/{gps_data_id}", response_model=gps_data_schema.GpsData_get)
def read_gps_data_by_id(gps_data_id: int, DB: Session = Depends(get_DB)):
    """
    Retrieve a single GPS record by its unique ID.

    Args:
        gps_data_id (int): The unique identifier of the GPS record.
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Raises:
        HTTPException(404): If no GPS data exists with the given ID.

    Returns:
        GpsData_get: The GPS record serialized with Pydantic.
    """
    db_gps_data = gps_data_repo.get_gps_data_by_id(DB, gps_data_id=gps_data_id)
    if db_gps_data is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    return db_gps_data

@router.post("/post", response_model=gps_data_schema.GpsData_get)
def create_gps_data(gps_data: gps_data_schema.GpsData_create, DB: Session = Depends(get_DB)):
    """
    Create a new GPS data record in the database.

    Args:
        gps_data (GpsData_create): Pydantic model containing GPS data to create.
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Returns:
        GpsData_get: The newly created GPS record.
    """
    return gps_data_repo.created_gps_data(DB, gps_data)

@router.patch("/{gps_data_id}", response_model=gps_data_schema.GpsData_get)
def update_gps_data(gps_data_id: int, gps_data: gps_data_schema.GpsData_update, DB: Session = Depends(get_DB)):
    """
    Update an existing GPS record.

    Args:
        gps_data_id (int): Unique identifier of the GPS record to update.
        gps_data (GpsData_update): Pydantic model containing the fields to update.
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Raises:
        HTTPException(404): If no GPS data exists with the given ID.

    Returns:
        GpsData_get: The updated GPS record.
    """
    updated = gps_data_repo.update_gps_data(DB, gps_data_id, gps_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    return updated

@router.delete("/{gps_data_id}", response_model=gps_data_schema.GpsData_delete)
def delete_gps_data(gps_data_id: int, DB: Session = Depends(get_DB)):
    """
    Delete a GPS record by its unique ID.

    Args:
        gps_data_id (int): Unique identifier of the GPS record to delete.
        DB (Session, optional): SQLAlchemy database session injected via Depends(get_DB).

    Raises:
        HTTPException(404): If no GPS data exists with the given ID.

    Returns:
        dict: A dictionary containing the ID of the deleted record.
    """
    deleted_id = gps_data_repo.delete_gps_data(DB, gps_data_id)
    if deleted_id is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    return {"id": deleted_id}