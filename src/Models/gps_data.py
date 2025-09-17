# src/Models/gps_data.py
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, Float, BigInteger, DateTime
from src.DB.base_class import Base

class GPS_data(Base):
    """
    SQLAlchemy model for storing GPS data.
    Table name is dynamically generated using declared_attr.directive,
    which allows for future flexibility while remaining compatible with type checkers.
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Dynamic table name logic.
        # Currently fixed as "gps_data" for consistency.
        return "gps_data"

    # Primary key
    id = Column(BigInteger, primary_key=True, autoincrement=True)

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
