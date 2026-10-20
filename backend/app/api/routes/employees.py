"""
Employee API routes.

GET /employees – search with pagination.
Query params validated by Pydantic schema. Business logic in service layer.
"""

import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.employee import (
    EmployeeResponse,
    ErrorResponse,
    PaginatedResponse,
)
from app.services.employee_service import EmployeeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get(
    "",
    response_model=PaginatedResponse[EmployeeResponse],
    responses={
        422: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "Database unavailable"},
    },
    summary="Search employees",
    description="Search employees by name or department with pagination.",
)
def search_employees(
    search: str = Query(
        default="",
        max_length=100,
        description="Search term – matches employee name or department",
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
        description="Maximum results per page",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of results to skip",
    ),
    db: Session = Depends(get_db),
) -> PaginatedResponse[EmployeeResponse]:
    """
    Search the employee directory.

    - Empty search returns a paginated list of all employees.
    - Matches against name or department (case-insensitive substring).
    - Results are ordered by employee ID for stable pagination.
    """
    search_term = search.strip()

    try:
        service = EmployeeService(db)
        return service.search_employees(
            search_term=search_term,
            limit=limit,
            offset=offset,
        )
    except OperationalError:
        logger.exception("Database connection failure during employee search")
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail="Database is temporarily unavailable. Please try again shortly.",
        )
    except Exception:
        logger.exception("Unexpected error during employee search")
        from fastapi import HTTPException

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again.",
        )
