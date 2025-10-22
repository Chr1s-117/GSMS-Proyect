# src/Models/gps_data.py
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, BigInteger, String, Float, DateTime, CheckConstraint, Index
from src.DB.base_class import Base


class GPS_data(Base):
    """
    SQLAlchemy model for storing GPS data from multiple devices.
    
    Responsibilities:
    - Store GPS telemetry data (latitude, longitude, altitude, accuracy, timestamp)
    - Associate GPS data with specific devices via DeviceID
    - Track geofence relationships (current geofence, event types)
    - Support efficient multi-device queries via composite indexes
    - Prevent duplicate GPS readings per device via unique constraint
    
    Schema:
    - id (PK): Auto-incrementing primary key
    - DeviceID: Identifier of the GPS device (indexed)
    - Latitude, Longitude: GPS coordinates in WGS84
    - Altitude: Elevation in meters
    - Accuracy: GPS accuracy in meters
    - Timestamp: UTC timestamp of GPS reading (required)
    - CurrentGeofenceID: ID of geofence containing this point (null if outside)
    - CurrentGeofenceName: Cached geofence name for quick display
    - GeofenceEventType: Event type (entry, exit, inside) if applicable
    
    Indexes:
    - idx_device_id_desc: Efficient "last GPS per device" queries
    - idx_device_id_asc: Efficient "oldest GPS per device" queries
    - idx_device_timestamp: Time-range queries per device
    - idx_device_geofence: Geofence-filtered queries per device
    - idx_geofence_timestamp: Time-range queries per geofence
    - unique_device_timestamp: Prevents duplicate readings
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Fixed table name for the GPS data
        return "gps_data"

    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # Device identifier (NEW: multi-device support)
    DeviceID = Column(
        String(100),
        nullable=False,
        index=True,  # Simple index for basic queries
        doc="Unique identifier of the GPS device"
    )

    # GPS fields
    Latitude = Column(Float, nullable=False)
    Longitude = Column(Float, nullable=False)
    Altitude = Column(Float, nullable=False)
    Accuracy = Column(Float, nullable=False)

    # Timestamp stored as timezone-aware DateTime (UTC)
    # No default: the value must be provided; otherwise the row will not be inserted.
    Timestamp = Column(
        DateTime(timezone=True),
        nullable=False
    )

    # Geofence-related fields (NEW: geofence integration)
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
        # Descending index for "last GPS per device" queries (most recent first)
        Index('idx_device_id_desc', DeviceID, id.desc()),
        
        # Ascending index for "oldest GPS per device" queries
        Index('idx_device_id_asc', DeviceID, id.asc()),
        
        # Time-range queries per device
        Index('idx_device_timestamp', DeviceID, Timestamp),
        
        # Geofence-filtered queries per device
        Index('idx_device_geofence', DeviceID, CurrentGeofenceID),
        
        # Time-range queries per geofence (e.g., "all GPS in warehouse X today")
        Index('idx_geofence_timestamp', CurrentGeofenceID, Timestamp),
        
        # Prevent duplicate GPS readings from same device at same timestamp
        Index('unique_device_timestamp', DeviceID, Timestamp, unique=True),
        
        # Validate GeofenceEventType values
        CheckConstraint(
            '"GeofenceEventType" IN (\'entry\', \'exit\', \'inside\')', 
            name='check_geofence_event_type'
        ),
    )

    def __repr__(self) -> str:
        """
        Returns a concise string representation for debugging and logging.
        Example: <GPS_data(id=12345, DeviceID='TRUCK-001', Lat=10.9878, Lon=-74.7889)>
        """
        return (
            f"<GPS_data(id={self.id}, DeviceID={self.DeviceID!r}, "
            f"Lat={self.Latitude:.4f}, Lon={self.Longitude:.4f})>"
        )