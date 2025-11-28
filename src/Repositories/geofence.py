# src/Repositories/geofence.py

from sqlalchemy.orm import Session
from src.Models.geofence import Geofence
from typing import List, Optional


def get_all_geofences(db: Session, only_active: bool = True) -> List[Geofence]:
    """
    Obtiene todas las geocercas.
    
    Args:
        db: Session SQLAlchemy
        only_active: Si True, solo retorna geocercas activas
    """
    query = db.query(Geofence)
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.all()


def get_geofence_by_id(db: Session, geofence_id: str) -> Optional[Geofence]:
    """Obtiene una geocerca por ID."""
    return db.query(Geofence).filter(Geofence.id == geofence_id).first()


def create_geofence(db: Session, geofence_data: dict) -> Geofence:
    """
    Crea una nueva geocerca.
    
    Args:
        db: Session SQLAlchemy
        geofence_data: Dict con datos de la geocerca
    """
    new_geofence = Geofence(**geofence_data)
    db.add(new_geofence)
    db.commit()
    db.refresh(new_geofence)
    return new_geofence


def update_geofence(db: Session, geofence_id: str, update_data: dict) -> Optional[Geofence]:
    """Actualiza una geocerca existente."""
    geofence = get_geofence_by_id(db, geofence_id)
    
    if not geofence:
        return None
    
    for key, value in update_data.items():
        if hasattr(geofence, key):
            setattr(geofence, key, value)
    
    db.commit()
    db.refresh(geofence)
    return geofence


def delete_geofence(db: Session, geofence_id: str) -> bool:
    """Elimina una geocerca."""
    geofence = get_geofence_by_id(db, geofence_id)
    
    if not geofence:
        return False
    
    db.delete(geofence)
    db.commit()
    return True


def count_geofences(db: Session, only_active: bool = True) -> int:
    """Cuenta geocercas en la DB."""
    query = db.query(Geofence)
    
    if only_active:
        query = query.filter(Geofence.is_active == True)
    
    return query.count()