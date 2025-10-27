# src/Models/geofence.py

"""
Geofence Model - Geographic Boundary Definitions

This module defines the SQLAlchemy model for geofences (geographic fences)
using PostGIS spatial extensions for PostgreSQL.

Geofences are polygon-shaped zones used to trigger events when GPS devices
enter, exit, or remain inside specific geographic areas (warehouses, delivery
zones, restricted areas, etc.).

Database Table: geofences
Primary Key: id (String)
Spatial Extension: PostGIS (Geography type with SRID 4326)

Dependencies:
    - PostgreSQL with PostGIS extension enabled
    - geoalchemy2 library for spatial column support
    - SRID 4326 = WGS84 standard GPS coordinates (latitude/longitude)

Usage:
    from src.Models.geofence import Geofence
    from src.DB.session import SessionLocal
    from geoalchemy2.shape import from_shape
    from shapely.geometry import Polygon
    
    db = SessionLocal()
    polygon = Polygon([
        (-74.006, 40.7128),  # lng, lat
        (-74.005, 40.7128),
        (-74.005, 40.7138),
        (-74.006, 40.7138),
        (-74.006, 40.7128)
    ])
    
    geofence = Geofence(
        id="warehouse-nyc-001",
        name="NYC Main Warehouse",
        description="Primary distribution center",
        geometry=from_shape(polygon, srid=4326),
        type="warehouse",
        is_active=True,
        color="#FF5733"
    )
    db.add(geofence)
    db.commit()
"""

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
    - extra_metadata: JSONB field for flexible additional data
    - created_at: Timestamp when geofence was created
    - updated_at: Timestamp of last modification
    
    Spatial Features:
    - Uses Geography type for accurate distance calculations on Earth's surface
    - SRID 4326 = WGS84 standard GPS coordinates (latitude/longitude)
    - Supports spatial indexes for efficient queries (configured in Alembic migrations)
    
    PostGIS Requirements:
    - PostgreSQL must have PostGIS extension enabled: CREATE EXTENSION postgis;
    - Spatial indexes recommended: CREATE INDEX idx_geofences_geometry ON geofences USING GIST(geometry);
    
    Performance Considerations:
    - Geography type uses spherical calculations (more accurate but slower)
    - For high-frequency queries, consider caching active geofences in memory
    - Spatial indexes are critical for performance with large datasets
    """
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Fixed table name for geofences"""
        return "geofences"
    
    # ============================================================
    # Primary Key
    # ============================================================
    id = Column(
        String(100), 
        primary_key=True,
        doc="Unique identifier for the geofence (e.g., 'warehouse-001', 'zone-delivery-nyc')"
    )
    
    # ============================================================
    # Geofence Metadata
    # ============================================================
    name = Column(
        String(200), 
        nullable=False,
        doc="Human-readable geofence name for display in UI"
    )
    
    description = Column(
        Text, 
        nullable=True,
        doc="Detailed description of the geofence purpose or location"
    )
    
    # ============================================================
    # Spatial Geometry Field (PostGIS)
    # ============================================================
    geometry = Column(
        Geography('POLYGON', srid=4326), 
        nullable=False,
        doc=(
            "PostGIS POLYGON geometry in WGS84 coordinates (SRID 4326). "
            "Represents the geographic boundary of the geofence. "
            "Use Geography type for accurate distance calculations on Earth's surface."
        )
    )
    
    # ============================================================
    # Classification and State
    # ============================================================
    type = Column(
        String(50), 
        default='custom', 
        nullable=False,
        doc="Geofence classification (e.g., 'warehouse', 'delivery_zone', 'restricted', 'custom')"
    )
    
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        doc="Whether geofence is currently active for event detection"
    )
    
    # ============================================================
    # Visualization
    # ============================================================
    color = Column(
        String(7), 
        default='#3388ff', 
        nullable=False,
        doc="Hex color code for map visualization (e.g., '#FF5733', '#3388ff')"
    )
    
    # ============================================================
    # Flexible Metadata Storage
    # ============================================================
    extra_metadata = Column(
        'metadata',  # Column name in database
        JSONB, 
        nullable=True,
        doc=(
            "Flexible JSON metadata for storing additional geofence properties. "
            "Examples: contact info, alert rules, custom tags, etc."
        )
    )
    
    # ============================================================
    # Timestamps
    # ============================================================
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when geofence was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now(),
        nullable=True,
        doc="Timestamp of last modification (automatically updated on changes)"
    )
    
    def __repr__(self) -> str:
        """
        Returns a concise string representation for debugging and logging.
        
        Example:
            <Geofence(id='warehouse-001', name='Main Warehouse', is_active=True)>
        """
        return (
            f"<Geofence(id={self.id!r}, name={self.name!r}, "
            f"is_active={self.is_active})>"
        )