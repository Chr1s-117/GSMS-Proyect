# src/Models/geofence.py

from sqlalchemy import Column, String, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declared_attr
from geoalchemy2 import Geography
from src.DB.base_class import Base

class Geofence(Base):
    """
    Modelo de geocercas (geofences) con geometría espacial PostGIS.
    
    Almacena polígonos que representan zonas de interés:
    - Almacenes, zonas industriales, puntos de entrega, etc.
    """
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Fixed table name for the GPS data
        return "geofences"
    
    id = Column(String(100), primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Campo espacial: almacena POLYGON en formato GEOGRAPHY (coordenadas esféricas)
    # SRID 4326 = WGS84 (latitud/longitud estándar GPS)
    geometry = Column(
        Geography('POLYGON', srid=4326), 
        nullable=False
    )
    
    type = Column(String(50), default='custom')
    is_active = Column(Boolean, default=True, nullable=False)
    color = Column(String(7), default='#3388ff')
    extra_metadata = Column('metadata', JSONB, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Geofence(id={self.id!r}, name={self.name!r})>"