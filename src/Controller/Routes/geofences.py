from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.Controller.deps import get_DB
from src.Repositories import geofence as geofence_repo
from src.Schemas import geofence as geofence_schema

router = APIRouter()

@router.get("/")
def list_geofences(db: Session = Depends(get_DB)):
    return geofence_repo.get_all_geofences(db)

@router.post("/")
def create_geofence(geofence: geofence_schema.GeofenceCreate, db: Session = Depends(get_DB)):
    return geofence_repo.create_geofence(db, geofence)