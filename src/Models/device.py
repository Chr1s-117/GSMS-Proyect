# src/Models/device.py

from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from src.DB.base_class import Base


class Device(Base):
    """
    SQLAlchemy model representing a registered GPS device.

    Responsibilities:
    - Tracks all registered and authorized GPS devices.
    - Associates human-readable names and descriptions with each device.
    - Maintains activation state without deleting historical data.
    - Records creation and last connection timestamps.

    Schema:
    - DeviceID (PK): Unique identifier for GPS device (e.g., "TRUCK-001")
    - Name: Human-readable device name (optional)
    - Description: Additional information about device (optional)
    - IsActive: Whether device is currently active (default: True)
    - CreatedAt: Timestamp when device was registered
    - LastSeen: Last activity timestamp from device
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Fixed table name for the device registry
        return "devices"

    # Primary key — unique identifier for the GPS device
    DeviceID = Column(String(100), primary_key=True)

    # Device metadata
    Name = Column(String(200), nullable=True)
    Description = Column(String(500), nullable=True)

    # Operational state
    IsActive = Column(Boolean, default=True, nullable=False)

    # Timestamps
    CreatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp of record creation."
    )
    LastSeen = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last time the device reported activity."
    )

    def __repr__(self) -> str:
        """
        Returns a concise string representation for debugging and logging.
        Example: <Device(DeviceID='TRUCK-001', Name='Main Fleet Truck', IsActive=True)>
        """
        return (
            f"<Device(DeviceID={self.DeviceID!r}, "
            f"Name={self.Name!r}, IsActive={self.IsActive})>"
        )