"""
Database engine and session management.

Creates a single engine with connection pooling and exposes an async-compatible
session factory via FastAPI's dependency injection system.

Design decisions:
- pool_pre_ping=True catches stale MySQL connections before they cause 500s.
- pool_recycle keeps connections alive within MySQL's wait_timeout.
- Scoped session ensures each request gets its own unit-of-work.
"""

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

engine_kwargs = {
    "echo": settings.DEBUG,
}

if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True,
    })

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.

    Guarantees the connection is returned to the pool even if the
    request handler raises an exception.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
