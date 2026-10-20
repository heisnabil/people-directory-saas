"""
SQLAlchemy declarative base.

All ORM models inherit from this base so Alembic can auto-detect schema changes.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass
