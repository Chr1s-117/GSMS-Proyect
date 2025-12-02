"""
src/DB/base_class.py
=================================
SQLAlchemy Base Model Definition
=================================

This module defines the declarative base class for all database models in the
GPS tracking application. It provides automatic table naming convention and
ensures compatibility with modern SQLAlchemy 2.0+ practices.

Architecture:
------------
- Extends SQLAlchemy's DeclarativeBase (2.0 style)
- Implements automatic table naming convention (class name → lowercase table name)
- Provides type-safe model inheritance for all application models

Compatibility:
-------------
- SQLAlchemy 2.0+: Uses DeclarativeBase instead of deprecated declarative_base()
- Alembic: Fully compatible with automatic migration generation
- FastAPI: Integrates seamlessly with Pydantic models and dependency injection
- Type Checkers: Works with mypy, Pylance, and other static analysis tools

Usage Example:
-------------
    from src.DB.base_class import Base
    from sqlalchemy import Column, Integer, String
    
    class Device(Base):
        # Table name automatically becomes 'device'
        id = Column(Integer, primary_key=True)
        name = Column(String(100))
        imei = Column(String(15), unique=True)
    
    # The Device model will create a table named 'device' in the database

Convention:
----------
Table names are derived from class names using lowercase conversion:
    - GPS_data → gps_data
    - Device → device
    - AccelerometerData → accelerometerdata
    - Trip → trip

Note:
    All application models must inherit from this Base class to be properly
    registered with SQLAlchemy's metadata and discovered by Alembic migrations.
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models in the application.
    
    This class provides the foundation for all database models, implementing
    automatic table naming convention and ensuring proper metadata registration
    for migration tools and ORM functionality.
    
    Features:
        - Automatic table naming: Converts class name to lowercase
        - Metadata registration: All models are registered in Base.metadata
        - Type safety: Compatible with modern type checkers (mypy, Pylance)
        - Alembic integration: Enables automatic migration generation
    
    Class Attributes:
        __tablename__: Automatically generated from class name (lowercase)
    
    Example:
        class UserAccount(Base):
            # Table name will be 'useraccount'
            id = Column(Integer, primary_key=True)
            username = Column(String(50))
    """
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Generate table name from class name using lowercase convention.
        
        This directive is executed when the model class is defined, automatically
        setting the database table name based on the class name.
        
        Args:
            cls: The model class being defined
            
        Returns:
            str: Lowercase version of the class name
            
        Examples:
            GPS_data → 'gps_data'
            Device → 'device'
            AccelerometerData → 'accelerometerdata'
        """
        return cls.__name__.lower()