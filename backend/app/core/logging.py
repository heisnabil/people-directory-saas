"""
Structured logging configuration.

Configures stdlib logging with a JSON-friendly format for production
and a readable format for development.
"""

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    """Configure root logger based on application settings."""
    settings = get_settings()

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        if settings.APP_ENV == "development"
        else '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
    )

    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format=log_format,
        datefmt="%Y-%m-%dT%H:%M:%S",
        stream=sys.stdout,
        force=True,
    )

    # Reduce noise from chatty libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
