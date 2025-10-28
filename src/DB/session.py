#src/DB/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Core.config import settings


"""
Here the session configuration will be set up to allow create a connection to the database.
Config here Data processes's parameters and settings.

"""
# Create SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
