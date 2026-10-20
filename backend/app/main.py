"""
FastAPI application factory.

Creates the application instance, configures CORS, registers routers,
and sets up global exception handling.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging

# Configure logging before anything else
setup_logging()

logger = logging.getLogger(__name__)
settings = get_settings()


def create_app() -> FastAPI:
    """Build and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # --- CORS ---
    # Restricted to configured origins (defaults to the Vite dev server).
    # Not using allow_origins=["*"] to avoid accidental exposure.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET"],  # This API is read-only
        allow_headers=["*"],
    )

    # --- Routers ---
    app.include_router(api_router)

    # --- Global exception handler ---
    # Catches anything that slips past route-level handling.
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please try again."},
        )

    logger.info(
        "Application started — env=%s, cors=%s",
        settings.APP_ENV,
        settings.cors_origin_list,
    )

    return app


app = create_app()
