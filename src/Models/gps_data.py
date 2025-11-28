# src/Models/gps_data.py
from sqlalchemy.orm import declared_attr
from sqlalchemy import (
    Column, BigInteger, String, Float, DateTime,
    CheckConstraint, func, Index, ForeignKeyConstraint
)
from src.DB.base_class import Base


class GPS_data(Base):
    """
    SQLAlchemy model for storing GPS data.
    Table name is dynamically generated using declared_attr.directive,
    which allows for future flexibility while remaining compatible with type checkers.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Fixed table name for the GPS data
        return "gps_data"

    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # NUEVO: Device identifier
    DeviceID = Column(
        String(100),
        nullable=False,
        index=True,  # Índice simple
        doc="Unique identifier of the GPS device"
    )

    # ========================================
    # TRIP RELATIONSHIP (NUEVO)
    # ========================================
    trip_id = Column(
        String(100),
        nullable=True,  # NULL for legacy data (pre-trip implementation)
        index=True,
        doc="ID of the trip this GPS point belongs to (NULL for historical data)"
    )

    # GPS fields
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    Altitude = Column(Float, nullable=False)
    Accuracy = Column(Float, nullable=False)

    # Timestamp stored as timezone-aware DateTime (UTC)
    Timestamp = Column(
        DateTime(timezone=True),
        nullable=False
    )

    # Geofence-related fields
    CurrentGeofenceID = Column(
        String(100),
        nullable=True,
        index=True,
        doc="ID of geofence containing this GPS point (null if outside all geofences)"
    )

    CurrentGeofenceName = Column(
        String(200),
        nullable=True,
        doc="Cached geofence name for quick display without JOIN"
    )

    GeofenceEventType = Column(
        String(10),
        nullable=True,
        doc="Event type if this GPS triggered a geofence transition: entry, exit, inside"
    )

    # Composite indexes for efficient multi-device queries
    __table_args__ = (
        # Existing indexes
        Index('idx_device_id_desc', DeviceID, id.desc()),
        Index('idx_device_id_asc', DeviceID, id.asc()),
        Index('idx_device_timestamp', DeviceID, Timestamp),
        Index('idx_device_geofence', DeviceID, CurrentGeofenceID),
        Index('idx_geofence_timestamp', CurrentGeofenceID, Timestamp),
        Index('unique_device_timestamp', DeviceID, Timestamp, unique=True),

        # ========================================
        # NUEVOS: Trip-related indexes
        # ========================================
        Index('idx_gps_trip_id', 'trip_id'),
        Index('idx_gps_trip_timestamp', 'trip_id', Timestamp.asc()),

        # ========================================
        # NUEVO: Foreign Key to trips
        # ========================================
        ForeignKeyConstraint(
            ['trip_id'],
            ['trips.trip_id'],
            name='fk_gps_data_trip_id',
            ondelete='SET NULL'  # If trip deleted, GPS points remain with trip_id=NULL
        ),

        # Existing check constraint
        CheckConstraint(
            '"GeofenceEventType" IN (\'entry\', \'exit\', \'inside\')',
            name='check_geofence_event_type'
        ),
    )

    # Optional: for debugging and clean logging
    def __repr__(self) -> str:
        return (
            f"<GPS_data(id={self.id}, DeviceID={self.DeviceID!r}, "
            f"Lat={self.Latitude:.4f}, Lon={self.Longitude:.4f}, trip_id={self.trip_id!r})>"
        )
