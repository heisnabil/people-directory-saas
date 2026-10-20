"""
Health check endpoint.

Verifies that the API is running and the database is reachable.
Useful for load balancers and monitoring.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
def health_check(db: Session = Depends(get_db)) -> dict:
    """
    Returns service health status.
    Performs a lightweight DB query to confirm connectivity.
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "ok" if db_status == "healthy" else "degraded",
        "database": db_status,
    }
