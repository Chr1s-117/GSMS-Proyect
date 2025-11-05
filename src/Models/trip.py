# src/Models/trip.py
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import declared_attr
from src.DB.base_class import Base


class Trip(Base):
    """
    SQLAlchemy model for trip metadata (movement and parking sessions).
    
    Responsibilities:
    - Stores aggregated trip information (start, end, metrics)
    - Links GPS points through trip_id foreign key
    - Maintains pre-calculated metrics (distance, duration, speed)
    - Distinguishes between movement trips and parking sessions
    
    Related models:
    - Device (1:N) - one device has many trips
    - GPS_data (1:N) - one trip contains many GPS points
    """
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "trips"
    
    # ========================================
    # PRIMARY KEY
    # ========================================
    trip_id = Column(
        String(100), 
        primary_key=True,
        doc="Unique trip identifier (format: TRIP_YYYYMMDD_DEVICE_NNN or PARKING_...)"
    )
    
    # ========================================
    # FOREIGN KEY
    # ========================================
    device_id = Column(
        String(100),
        ForeignKey('devices.DeviceID', ondelete='CASCADE'),
        nullable=False,
        index=True,
        doc="Device that generated this trip"
    )
    
    # ========================================
    # TRIP CLASSIFICATION
    # ========================================
    trip_type = Column(
        String(20),
        nullable=False,
        doc="Trip type: 'movement' (vehicle in motion) or 'parking' (stationary session)"
    )
    
    status = Column(
        String(20),
        nullable=False,
        server_default='active',
        doc="Trip status: 'active' (ongoing) or 'closed' (completed)"
    )
    
    # ========================================
    # TEMPORAL BOUNDS
    # ========================================
    start_time = Column(
        DateTime(timezone=True),
        nullable=False,
        doc="UTC timestamp of first GPS point in trip"
    )
    
    end_time = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="UTC timestamp of last GPS point (NULL if trip is active)"
    )
    
    # ========================================
    # SPATIAL BOUNDS (Start Location)
    # ========================================
    start_lat = Column(
        Float,
        nullable=False,
        doc="Latitude of trip start point (decimal degrees)"
    )
    
    start_lon = Column(
        Float,
        nullable=False,
        doc="Longitude of trip start point (decimal degrees)"
    )
    
    # ========================================
    # PRE-CALCULATED METRICS
    # ========================================
    distance = Column(
        Float,
        nullable=True,
        server_default='0.0',
        doc="Total distance traveled in meters (calculated on trip close)"
    )
    
    duration = Column(
        Float,
        nullable=True,
        server_default='0.0',
        doc="Total duration in seconds (end_time - start_time)"
    )
    
    avg_speed = Column(
        Float,
        nullable=True,
        doc="Average speed in km/h (distance / duration * 3.6)"
    )
    
    point_count = Column(
        Integer,
        nullable=False,
        server_default='0',
        doc="Number of GPS points in this trip"
    )
    
    # ========================================
    # AUDIT FIELDS
    # ========================================
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when trip record was created"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        doc="Timestamp of last update"
    )
    
    # ========================================
    # TABLE CONSTRAINTS
    # ========================================
    __table_args__ = (
        # Composite indexes for efficient queries
        Index('idx_trips_device_status', 'device_id', 'status'),
        Index('idx_trips_device_start_time', 'device_id', 'start_time'),
        Index('idx_trips_device_type', 'device_id', 'trip_type'),
        
        # Validation constraints
        CheckConstraint(
            "trip_type IN ('movement', 'parking')",
            name='check_trip_type'
        ),
        CheckConstraint(
            "status IN ('active', 'closed')",
            name='check_status'
        ),
        CheckConstraint(
            "end_time IS NULL OR end_time >= start_time",
            name='check_time_order'
        ),
        CheckConstraint(
            "start_lat >= -90 AND start_lat <= 90",
            name='check_lat_range'
        ),
        CheckConstraint(
            "start_lon >= -180 AND start_lon <= 180",
            name='check_lon_range'
        ),
    )
    
    def __repr__(self) -> str:
        return (
            f"<Trip(trip_id={self.trip_id!r}, device_id={self.device_id!r}, "
            f"type={self.trip_type!r}, status={self.status!r})>"
        )