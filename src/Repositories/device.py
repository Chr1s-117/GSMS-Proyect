from sqlalchemy.orm import Session
from src.Models.device import Device
from src.Schemas.device import Device_create, Device_update

def get_all_devices(db: Session):
    return db.query(Device).all()

def create_device(db: Session, device: Device_create):
    new_device = Device(**device.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device