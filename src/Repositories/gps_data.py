# src/Repositories/gps_data.py

from sqlalchemy.orm import Session
from src.Models.gps_data import GPS_data
from src.Schemas.gps_data import GpsData_create, GpsData_update
from src.Services.gps_serialization import serialize_gps_row, serialize_many
from datetime import datetime
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
def get_last_gps_row(DB: Session, include_id: bool = False) -> dict | None:
    row = DB.query(GPS_data).order_by(GPS_data.id.desc()).first()
    return serialize_gps_row(row, include_id=include_id)
"""
Retrieve the oldest GPS_data row from the database.
Returns None if the table is empty.

This allows the system to fetch the starting point of the historical route.
"""
def get_oldest_gps_row(DB: Session, include_id: bool = False) -> dict | None:
    row = DB.query(GPS_data).order_by(GPS_data.id.asc()).first()
    return serialize_gps_row(row, include_id=include_id)

"""
Retrieve GPS data within a given time range [start_time, end_time].

    Args:
        DB: SQLAlchemy session
        start_time: datetime (inclusive lower bound)
        end_time: datetime (inclusive upper bound)
        include_id: include DB primary key in payload

Returns: List of dicts (JSON-serializable) already serialized with ISO-8601 UTC timestamps
"""

def get_gps_data_in_range(DB: Session, start_time: datetime, end_time: datetime, include_id: bool = False) -> list[dict]:
    rows = (
        DB.query(GPS_data)
        .filter(GPS_data.Timestamp >= start_time, GPS_data.Timestamp <= end_time)
        .order_by(GPS_data.Timestamp.asc())
        .all()
    )

    return serialize_many(rows, include_id=include_id)

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
