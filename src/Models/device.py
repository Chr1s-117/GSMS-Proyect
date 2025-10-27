# src/Models/device.py

"""
Device Model - GPS Device Registry

This module defines the SQLAlchemy model for registered GPS tracking devices.

The Device table serves as the authoritative registry of all GPS devices
allowed to send data to the system. It tracks device metadata, activation
state, and connectivity status.

Database Table: devices
Primary Key: DeviceID (String)

Usage:
    from src.Models.device import Device
    from src.DB.session import SessionLocal
    
    db = SessionLocal()
    device = Device(
        DeviceID="TRUCK-001",
        Name="Main Fleet Truck",
        Description="Primary delivery vehicle",
        IsActive=True
    )
    db.add(device)
    db.commit()
"""

from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from src.DB.base_class import Base


class Device(Base):
    """
    SQLAlchemy model representing a registered GPS device.

    Responsibilities:
    - Tracks all registered and authorized GPS devices
    - Associates human-readable names and descriptions with each device
    - Maintains activation state without deleting historical data
    - Records creation and last connection timestamps

    Schema:
    - DeviceID (PK): Unique identifier for GPS device (e.g., "TRUCK-001")
    - Name: Human-readable device name (optional)
    - Description: Additional information about device (optional)
    - IsActive: Whether device is currently active (default: True)
    - CreatedAt: Timestamp when device was registered
    - LastSeen: Last activity timestamp from device

    Relationships:
    - One-to-many with GPS_data: A device can have many GPS records

    Indexes:
    - Primary key on DeviceID (automatic)
    - Consider adding index on LastSeen for queries filtering by recent activity
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Fixed table name for the device registry"""
        return "devices"

    # ============================================================
    # Primary Key
    # ============================================================
    DeviceID = Column(
        String(100), 
        primary_key=True,
        doc="Unique identifier for the GPS device (e.g., 'TRUCK-001', 'IMEI-123456')"
    )

    # ============================================================
    # Device Metadata
    # ============================================================
    Name = Column(
        String(200), 
        nullable=True,
        doc="Human-readable device name for display in UI"
    )
    
    Description = Column(
        String(500), 
        nullable=True,
        doc="Additional information about the device (location, owner, notes)"
    )

    # ============================================================
    # Operational State
    # ============================================================
    IsActive = Column(
        Boolean, 
        default=True, 
        nullable=False,
        doc="Whether device is currently active and allowed to send data"
    )

    # ============================================================
    # Timestamps
    # ============================================================
    CreatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        doc="Timestamp when device was registered in the system"
    )
    
    LastSeen = Column(
        DateTime(timezone=True),
        nullable=True,
        doc="Last time the device reported activity (updated on GPS data insert)"
    )

    def __repr__(self) -> str:
        """
        Returns a concise string representation for debugging and logging.
        
        Example:
            <Device(DeviceID='TRUCK-001', Name='Main Fleet Truck', IsActive=True)>
        """
        return (
            f"<Device(DeviceID={self.DeviceID!r}, "
            f"Name={self.Name!r}, IsActive={self.IsActive})>"
        )