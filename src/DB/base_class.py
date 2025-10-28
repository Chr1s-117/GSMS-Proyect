# src/DB/base_class.py
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    Automatically sets the __tablename__ to the lowercase class name.
    Compatible with Alembic, FastAPI, and type checkers (mypy/Pylance).
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
