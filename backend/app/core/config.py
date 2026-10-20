"""
Application configuration loaded from environment variables.

Uses pydantic-settings to validate and type-check all config at startup,
ensuring fast failure when required values are missing.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application settings validated against env vars."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    APP_ENV: str = "development"
    APP_NAME: str = "People Directory API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- Database ---
    DATABASE_URL: str = "mysql+pymysql://app_user:change_me@localhost:3306/employee_directory"

    # Pool tuning – conservative defaults appropriate for a small internal tool
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 1800  # seconds – avoids MySQL wait_timeout disconnects

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    # --- Search ---
    SEARCH_MAX_LENGTH: int = 100
    DEFAULT_PAGE_LIMIT: int = 20
    MAX_PAGE_LIMIT: int = 100

    @property
    def cors_origin_list(self) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached singleton – avoids re-reading .env on every request."""
    return Settings()
