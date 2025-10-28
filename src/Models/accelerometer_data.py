# src/Models/accelerometer_data.py

from sqlalchemy import Column, BigInteger, String, Float, Integer, SmallInteger, DateTime, Index
from sqlalchemy.orm import declared_attr
from src.DB.base_class import Base


class AccelerometerData(Base):
    """
    SQLAlchemy model for storing accelerometer statistics data.
    
    Linked to GPS data via composite key (DeviceID + Timestamp).
    Contains 5-second window statistics from vehicle motion sensors.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return "accelerometer_data"

    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 🔑 Composite index fields (same as gps_data)
    DeviceID = Column(
        String(100),
        nullable=False,
        index=True,
        doc="Device identifier (matches gps_data.DeviceID)"
    )
    
    Timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        doc="GPS timestamp (matches gps_data.Timestamp)"
    )

    # Accelerometer window timestamps
    ts_start = Column(
        DateTime(timezone=True),
        nullable=False,
        doc="Start of 5-second accelerometer window"
    )
    
    ts_end = Column(
        DateTime(timezone=True),
        nullable=False,
        doc="End of 5-second accelerometer window"
    )

    # RMS values (Root Mean Square) - sustained vibration
    rms_x = Column(Float, nullable=False, doc="RMS acceleration X-axis (g's)")
    rms_y = Column(Float, nullable=False, doc="RMS acceleration Y-axis (g's)")
    rms_z = Column(Float, nullable=False, doc="RMS acceleration Z-axis (g's)")
    rms_mag = Column(Float, nullable=False, doc="RMS vectorial magnitude (g's)")

    # Maximum absolute values - peak impacts
    max_x = Column(Float, nullable=False, doc="Max absolute acceleration X-axis (g's)")
    max_y = Column(Float, nullable=False, doc="Max absolute acceleration Y-axis (g's)")
    max_z = Column(Float, nullable=False, doc="Max absolute acceleration Z-axis (g's)")
    max_mag = Column(Float, nullable=False, doc="Max vectorial magnitude (g's)")

    # Statistical counters
    peaks_count = Column(
        Integer,
        nullable=False,
        doc="Number of samples exceeding threshold (default 1.5g)"
    )
    
    sample_count = Column(
        Integer,
        nullable=False,
        doc="Total samples in window (expected: 250)"
    )
    
    flags = Column(
        SmallInteger,
        nullable=False,
        default=0,
        doc="Validation flags bitmap (0 = valid window)"
    )

    # Table constraints and indexes
    __table_args__ = (
        # Unique constraint (prevents duplicates)
        Index(
            'unique_device_timestamp_accel',
            DeviceID,
            Timestamp,
            unique=True
        ),
        
        # Composite index for efficient queries
        Index(
            'idx_accel_device_timestamp',
            DeviceID,
            Timestamp
        ),
        
        # Descending index (for latest data queries)
        Index(
            'idx_accel_device_id_desc',
            DeviceID,
            id.desc()
        ),
        
        # Analytical indexes (partial - only high values)
        Index(
            'idx_accel_rms_mag_high',
            rms_mag,
            postgresql_where=(rms_mag > 0.3)
        ),
        
        Index(
            'idx_accel_max_mag_high',
            max_mag,
            postgresql_where=(max_mag > 2.0)
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<AccelerometerData(id={self.id}, DeviceID={self.DeviceID!r}, "
            f"Timestamp={self.Timestamp}, rms_mag={self.rms_mag:.3f}g, "
            f"max_mag={self.max_mag:.3f}g)>"
        )