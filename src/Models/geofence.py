# src/Models/geofence.py

from sqlalchemy import Column, String, Text, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declared_attr
from geoalchemy2 import Geography
from src.DB.base_class import Base


class Geofence(Base):
    """
    SQLAlchemy model representing geographic fence zones (geofences) with PostGIS spatial geometry.
    
    Responsibilities:
    - Store polygon geometries representing zones of interest (warehouses, delivery zones, etc.)
    - Support spatial queries (point-in-polygon, distance calculations, etc.)
    - Maintain activation state for enabling/disabling geofences
    - Track creation and modification timestamps
    - Store custom metadata for each geofence
    
    Schema:
    - id (PK): Unique identifier for the geofence
    - name: Human-readable name (e.g., "Main Warehouse")
    - description: Optional detailed description
    - geometry: PostGIS POLYGON in WGS84 (SRID 4326) spherical coordinates
    - type: Classification (e.g., "warehouse", "delivery_zone", "custom")
    - is_active: Whether geofence is currently active
    - color: Hex color for map visualization (default: #3388ff)
    - extra_metadata: JSON field for flexible additional data
    - created_at: Timestamp when geofence was created
    - updated_at: Timestamp of last modification
    
    Spatial Features:
    - Uses Geography type for accurate distance calculations on Earth's surface
    - SRID 4326 = WGS84 standard GPS coordinates (latitude/longitude)
    - Supports spatial indexes for efficient queries
    """
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Fixed table name for geofences
        return "geofences"
    
    # Primary key — unique identifier for the geofence
    id = Column(String(100), primary_key=True)
    
    # Geofence metadata
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Spatial field: stores POLYGON in GEOGRAPHY format (spherical coordinates)
    # SRID 4326 = WGS84 (standard GPS latitude/longitude)
    geometry = Column(
        Geography('POLYGON', srid=4326), 
        nullable=False
    )
    
    # Classification and state
    type = Column(String(50), default='custom', nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Visualization
    color = Column(String(7), default='#3388ff', nullable=False)
    
    # Flexible metadata storage
    extra_metadata = Column('metadata', JSONB, nullable=True)
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when geofence was created."
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now(),
        nullable=True,
        doc="Timestamp of last modification."
    )
    
    def __repr__(self) -> str:
        """
        Returns a concise string representation for debugging and logging.
        Example: <Geofence(id='warehouse-001', name='Main Warehouse')>
        """
        return f"<Geofence(id={self.id!r}, name={self.name!r})>"