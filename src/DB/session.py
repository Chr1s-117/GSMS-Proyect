"""
src/DB/session.py
======================================
Database Session Configuration Module
======================================

This module establishes the SQLAlchemy database connection and session management
configuration for the GPS tracking application. It provides the foundational
database infrastructure used throughout the application.

Architecture:
------------
- Engine: Manages the database connection pool and dialect
- SessionLocal: Factory for creating database sessions
- Configuration: Sourced from centralized settings module

Usage Example:
-------------
    from src.DB.session import SessionLocal
    
    # Create a new database session
    db = SessionLocal()
    try:
        # Perform database operations
        result = db.query(GPS_data).all()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
    
    # Or use context manager (recommended)
    with SessionLocal() as db:
        result = db.query(GPS_data).all()

Session Configuration:
---------------------
- autocommit=False: Transactions must be explicitly committed (ACID compliance)
- autoflush=False: Changes are not automatically flushed to database before queries
- bind=engine: Sessions are bound to the configured database engine

Note:
    The DATABASE_URL is retrieved from environment variables via the settings
    module, ensuring secure configuration management and environment-specific
    database connections.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Core.config import settings


# ============================================================
# DATABASE ENGINE CONFIGURATION
# ============================================================
# Create SQLAlchemy engine with connection pooling and dialect configuration
# The engine manages the database connection pool and handles low-level DBAPI interactions
engine = create_engine(settings.DATABASE_URL)


# ============================================================
# SESSION FACTORY CONFIGURATION
# ============================================================
# Create a configured session factory class
# SessionLocal() returns new Session instances for database operations
SessionLocal = sessionmaker(
    autocommit=False,  # Require explicit commit() for transaction control
    autoflush=False,   # Disable automatic flushing before queries for better control
    bind=engine        # Bind sessions to the configured database engine
)