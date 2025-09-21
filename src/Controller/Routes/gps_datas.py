# src/Controller/Routes/gps_datas.py

from fastapi import APIRouter, Depends, HTTPException
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
