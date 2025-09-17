# src/Controller/deps.py

from typing import Generator
from src.DB.session import SessionLocal

def get_DB() -> Generator:
    """
    Dependency generator for FastAPI endpoints that require a database session.

    Usage:
        from fastapi import Depends
        from src.Core.db import get_DB

        @app.get("/items")
        def read_items(db: Session = Depends(get_DB)):
            ...

    Behavior:
    - Opens a new SQLAlchemy session using SessionLocal().
    - Yields the session to the caller (endpoint or service).
    - Ensures the session is properly closed after use, even if an exception occurs.

    Returns:
        Generator[Session, None, None]: A SQLAlchemy session object.
    """
    DB = SessionLocal()  # Create a new database session
    try:
        yield DB  # Provide session to the caller
    finally:
        DB.close()  # Ensure the session is closed to release resources
