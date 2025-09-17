# src/Repositories/gps_data.py

from typing import Optional
from sqlalchemy.orm import Session
from src.Models.gps_data import GPS_data
from src.Schemas.gps_data import GpsData_create, GpsData_update

"""
get_gps_data to get all GPS data (from one user)
"""
def get_gps_data(DB: Session):
    return DB.query(GPS_data).all()

"""
get_gps_data_by_id to get GPS data (from one user) by ID
"""
def get_gps_data_by_id(DB: Session, gps_data_id: int):
    return DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()

"""
Retrieve the latest GPS_data row from the database.
Returns None if the table is empty.

This allows the UDP module to compare incoming GPS data
against the last stored record to avoid duplicates
in a multi-backend, redundant setup.
"""
def get_last_gps_row(db: Session) -> Optional[GPS_data]:

    return db.query(GPS_data).order_by(GPS_data.id.desc()).first()

"""
created_gps_data to create a new GPS data row
"""
def created_gps_data(DB: Session, gps_data: GpsData_create):
    new_gps_data = GPS_data(**gps_data.model_dump(exclude_unset=True))
    DB.add(new_gps_data)
    DB.commit()
    DB.refresh(new_gps_data)
    return new_gps_data


"""
update_gps_data to update GPS data row by ID
"""
def update_gps_data(DB: Session, gps_data_id: int, gps_data: GpsData_update):
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if not db_gps_data:
        return None

    # just update the fields that were sent
    update_data = gps_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_gps_data, key, value)

    DB.commit()
    DB.refresh(db_gps_data)
    return db_gps_data

"""
delete_gps_data to delete GPS data row by ID
"""
def delete_gps_data(DB: Session, gps_data_id: int):
    db_gps_data = DB.query(GPS_data).filter(GPS_data.id == gps_data_id).first()
    if db_gps_data is None:
        return None
    DB.delete(db_gps_data)
    DB.commit()
    return db_gps_data.id
