# src/Models/gps_data.py

"""
GPS Data Model - GPS Tracking Records with Geofence Support

This module defines the SQLAlchemy model for storing GPS tracking data
from registered devices, with integrated geofence event detection.

The GPS_data table is the core time-series data store for all GPS coordinates
received from devices. It includes geofence association fields to track which
geofence (if any) contains each GPS point, enabling real-time entry/exit detection.

Database Table: gps_data
Primary Key: id (BigInteger, auto-increment)
High-Volume Table: Expect millions of rows in production

Performance Considerations:
    - Partitioning by DeviceID or Timestamp recommended for large datasets
    - Composite indexes on (DeviceID, Timestamp) for efficient device queries
    - Consider archiving old data to separate cold storage tables

Usage:
    from src.Models.gps_data import GPS_data
    from src.DB.session import SessionLocal
    from datetime import datetime, timezone
    
    db = SessionLocal()
    gps_point = GPS_data(
        DeviceID="TRUCK-001",
        Latitude=40.7128,
        Longitude=-74.0060,
        Altitude=10.5,
        Accuracy=5.0,
        Timestamp=datetime.now(timezone.utc),
        CurrentGeofenceID="warehouse-nyc-001",
        CurrentGeofenceName="NYC Main Warehouse",
        GeofenceEventType="entry"
    )
    db.add(gps_point)
    db.commit()
"""

from sqlalchemy.orm import declared_attr
from sqlalchemy import (
    Column, BigInteger, String, Float, DateTime, 
    CheckConstraint, Index
)
from src.DB.base_class import Base


class GPS_data(Base):
    """
    SQLAlchemy model for storing GPS tracking data with geofence association.
    
    Responsibilities:
    - Store GPS coordinates (latitude, longitude, altitude) from devices
    - Record accuracy and timestamp of each GPS reading
    - Associate GPS points with geofences (if inside a geofence boundary)
    - Track geofence entry/exit/inside events for alerting
    
    Schema:
    - id (PK): Auto-incrementing unique identifier
    - DeviceID: Foreign reference to registered device (indexed)
    - Latitude: GPS latitude in decimal degrees (-90 to +90)
    - Longitude: GPS longitude in decimal degrees (-180 to +180)
    - Altitude: Elevation in meters above sea level
    - Accuracy: GPS accuracy in meters (lower is better)
    - Timestamp: UTC timestamp of GPS reading (indexed)
    - CurrentGeofenceID: ID of containing geofence (null if outside all)
    - CurrentGeofenceName: Cached geofence name for quick display
    - GeofenceEventType: Event classification (entry/exit/inside)
    
    Indexes:
    - idx_device_id_desc: Fast latest-by-device queries
    - idx_device_timestamp: Time-range queries per device
    - idx_device_geofence: Device + geofence filtering
    - idx_geofence_timestamp: Geofence history queries
    - unique_device_timestamp: Prevents duplicate GPS readings
    
    Constraints:
    - GeofenceEventType must be one of: 'entry', 'exit', 'inside'
    
    Relationships:
    - Many-to-one with Device: GPS records belong to a device
    - Many-to-one with Geofence: GPS records reference a geofence (optional)
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Fixed table name for GPS data"""
        return "gps_data"

    # ============================================================
    # Primary Key
    # ============================================================
    id = Column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True,
        doc="Auto-incrementing unique identifier for each GPS record"
    )

    # ============================================================
    # Device Association
    # ============================================================
    DeviceID = Column(
        String(100),
        nullable=False,
        index=True,  # Simple index for device filtering
        doc="Unique identifier of the GPS device that sent this data"
    )

    # ============================================================
    # GPS Coordinates
    # ============================================================
    Latitude = Column(
        Float, 
        nullable=False,
        doc="GPS latitude in decimal degrees (range: -90 to +90)"
    )
    
    Longitude = Column(
        Float, 
        nullable=False,
        doc="GPS longitude in decimal degrees (range: -180 to +180)"
    )
    
    Altitude = Column(
        Float, 
        nullable=False,
        doc="Elevation in meters above sea level"
    )
    
    Accuracy = Column(
        Float, 
        nullable=False,
        doc="GPS accuracy/precision in meters (lower values = better accuracy)"
    )

    # ============================================================
    # Timestamp
    # ============================================================
    Timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        doc="UTC timestamp when GPS reading was recorded by the device"
    )

    # ============================================================
    # Geofence Association (NEW)
    # ============================================================
    CurrentGeofenceID = Column(
        String(100), 
        nullable=True,
        index=True,
        doc=(
            "ID of geofence containing this GPS point. "
            "Null if GPS point is outside all active geofences."
        )
    )
    
    CurrentGeofenceName = Column(
        String(200), 
        nullable=True,
        doc=(
            "Cached geofence name for quick display without JOIN. "
            "Denormalized for performance (avoids repeated geofence lookups)."
        )
    )
    
    GeofenceEventType = Column(
        String(10),
        nullable=True,
        doc=(
            "Event type if this GPS point triggered a geofence transition:\n"
            "- 'entry': Device entered a geofence\n"
            "- 'exit': Device exited a geofence\n"
            "- 'inside': Device remains inside a geofence\n"
            "Null if no geofence event detected."
        )
    )

    # ============================================================
    # Indexes and Constraints
    # ============================================================
    __table_args__ = (
        # Composite index for latest GPS per device (DESC order)
        Index('idx_device_id_desc', DeviceID, id.desc()),
        
        # Composite index for oldest GPS per device (ASC order)
        Index('idx_device_id_asc', DeviceID, id.asc()),
        
        # Composite index for time-range queries per device
        Index('idx_device_timestamp', DeviceID, Timestamp),
        
        # Composite index for device + geofence filtering
        Index('idx_device_geofence', DeviceID, CurrentGeofenceID),
        
        # Composite index for geofence history queries
        Index('idx_geofence_timestamp', CurrentGeofenceID, Timestamp),
        
        # Unique constraint: prevent duplicate GPS readings from same device at same time
        Index('unique_device_timestamp', DeviceID, Timestamp, unique=True),
        
        # Check constraint: validate geofence event type values
        CheckConstraint(
            '"GeofenceEventType" IN (\'entry\', \'exit\', \'inside\')', 
            name='check_geofence_event_type'
        ),
    )

    def __repr__(self) -> str:
        """
        Returns a concise string representation for debugging and logging.
        
        Example:
            <GPS_data(id=12345, DeviceID='TRUCK-001', Lat=40.7128, Lon=-74.0060)>
        """
        return (
            f"<GPS_data(id={self.id}, DeviceID={self.DeviceID!r}, "
            f"Lat={self.Latitude:.4f}, Lon={self.Longitude:.4f})>"
        )