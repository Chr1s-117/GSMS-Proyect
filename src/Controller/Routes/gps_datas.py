from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from src.Controller.deps import get_DB
from src.Repositories import gps_data as gps_data_repo
from src.Schemas import gps_data as gps_data_schema

router = APIRouter()

# ---------- SPECIAL GET ROUTES ----------
@router.get("/last", response_model=gps_data_schema.GpsData_get)
def get_last_gps_row(DB: Session = Depends(get_DB)):
    last_row = gps_data_repo.get_last_gps_row(DB, include_id=True)  
    if last_row is None:
        raise HTTPException(status_code=404, detail="No GPS data found")
    return last_row

@router.get("/oldest", response_model=gps_data_schema.GpsData_get)
def get_oldest_gps_row(DB: Session = Depends(get_DB)):
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
    Get all GPS data between two timestamps.
    """
    data = gps_data_repo.get_gps_data_in_range(DB, start, end, include_id=True)
    if not data:
        raise HTTPException(status_code=404, detail="No GPS data found in range")
    return data


# ---------- STANDARD CRUD ROUTES ----------

@router.get("/", response_model=List[gps_data_schema.GpsData_get])
def read_gps_data(DB: Session = Depends(get_DB)):
    return gps_data_repo.get_gps_data(DB)

@router.get("/{gps_data_id}",response_model=gps_data_schema.GpsData_get)
def read_gps_data_by_id(gps_data_id: int, DB: Session = Depends(get_DB)):
    db_gps_data = gps_data_repo.get_gps_data_by_id(DB, gps_data_id=gps_data_id)
    if db_gps_data is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    return db_gps_data

@router.post("/post", response_model=gps_data_schema.GpsData_get)
def create_gps_data(gps_data: gps_data_schema.GpsData_create, DB: Session = Depends(get_DB)):
    return gps_data_repo.created_gps_data(DB, gps_data)

@router.patch("/{gps_data_id}", response_model=gps_data_schema.GpsData_get)
def update_gps_data(gps_data_id: int, gps_data: gps_data_schema.GpsData_update, DB: Session = Depends(get_DB)):
    updated = gps_data_repo.update_gps_data(DB, gps_data_id, gps_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    return updated

@router.delete("/{gps_data_id}", response_model=gps_data_schema.GpsData_delete)
def delete_gps_data(gps_data_id: int, DB: Session = Depends(get_DB)):
    deleted_id = gps_data_repo.delete_gps_data(DB, gps_data_id)
    if deleted_id is None:
        raise HTTPException(status_code=404, detail="GPS data not found")
    return {"id": deleted_id}

