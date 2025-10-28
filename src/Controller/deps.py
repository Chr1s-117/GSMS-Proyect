#src/Controller/deps.py

from typing import Generator
from src.DB.session import SessionLocal

def get_DB() -> Generator:
    DB = SessionLocal()
    try:
        yield DB
    finally:
        DB.close()
