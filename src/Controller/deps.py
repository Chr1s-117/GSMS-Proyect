# src/Controller/deps.py

"""
FastAPI Dependency Injection Module

This module provides reusable dependencies for FastAPI endpoints,
primarily for database session management.

Dependencies defined here follow FastAPI's dependency injection pattern
and are used across routers to ensure consistent resource management.
"""

from typing import Generator
from src.DB.session import SessionLocal


def get_DB() -> Generator:
    """
    Dependency generator for FastAPI endpoints that require a database session.

    This function creates a new SQLAlchemy session, yields it to the caller,
    and ensures it is properly closed after use (even if an exception occurs).

    Usage:
        from fastapi import Depends
        from src.Controller.deps import get_DB

        @router.get("/items")
        def read_items(db: Session = Depends(get_DB)):
            # Use db session here
            items = db.query(Item).all()
            return items

    Behavior:
    - Opens a new SQLAlchemy session using SessionLocal()
    - Yields the session to the caller (endpoint or service)
    - Ensures the session is properly closed after use via finally block
    
    Environment Compatibility:
    - Local: DATABASE_URL from .env file
    - AWS: DATABASE_URL from /etc/gsms/env (injected by systemd)
    
    Returns:
        Generator[Session, None, None]: A SQLAlchemy session object
        
    Raises:
        Any database connection errors are propagated to the caller
    """
    DB = SessionLocal()  # Create a new database session
    try:
        yield DB  # Provide session to the caller
    finally:
        DB.close()  # Ensure the session is closed to release resources