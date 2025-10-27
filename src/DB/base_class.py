# src/DB/base_class.py

"""
SQLAlchemy Declarative Base Class

This module defines the base class for all SQLAlchemy ORM models.

Features:
- Automatic table naming: Class name → lowercase table name
- Compatible with Alembic migrations
- Type-safe with mypy/Pylance
- Modern SQLAlchemy 2.0+ syntax (DeclarativeBase)

Usage:
    from src.DB.base_class import Base
    
    class MyModel(Base):
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(50))
        # __tablename__ is automatically set to "mymodel"
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    
    Automatically sets the __tablename__ to the lowercase class name.
    
    Example:
        class GPS_data(Base):
            ...
        
        # Resulting table name: "gps_data"
    
    Compatible with:
    - Alembic migrations (auto-detection)
    - FastAPI dependency injection
    - Type checkers (mypy/Pylance)
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.
        
        Conversion rules:
        - GPS_data → gps_data
        - Device → device
        - Geofence → geofence
        
        Returns:
            str: Lowercase class name
        """
        return cls.__name__.lower()