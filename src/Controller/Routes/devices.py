from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.Controller.deps import get_DB
from src.Repositories import device as device_repo
from src.Schemas import device as device_schema

router = APIRouter()

@router.get("/")
def list_devices(db: Session = Depends(get_DB)):
    return device_repo.get_all_devices(db)

@router.post("/")
def register_device(device: device_schema.Device_create, db: Session = Depends(get_DB)):
    return device_repo.create_device(db, device)