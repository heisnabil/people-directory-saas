"""
Pydantic schemas for the Employee API.

Separates the public contract from internal ORM details:
- EmployeeResponse: what clients see (no internal fields leaked).
- EmployeeSearchParams: validated query parameters with bounds.
- PaginatedResponse: paginated envelope with total count.
"""

from datetime import date
from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Query parameter validation
# ---------------------------------------------------------------------------

class EmployeeSearchParams(BaseModel):
    """
    Validated search query parameters.

    - search: optional free-text term (capped at 100 chars).
    - limit: page size, 1..100, defaults to 20.
    - offset: pagination offset, >= 0, defaults to 0.
    """

    search: str = Field(default="", max_length=100, description="Search term for name or department")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum results per page")
    offset: int = Field(default=0, ge=0, description="Number of results to skip")

    @field_validator("search")
    @classmethod
    def strip_search(cls, v: str) -> str:
        """Normalize whitespace in search input."""
        return v.strip()


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class EmployeeResponse(BaseModel):
    """Public employee representation – only assignment-required fields."""

    id: int
    name: str
    email: str
    department: str
    designation: str
    date_of_joining: date

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated envelope with total count for the full matching set."""

    items: List[T]
    total: int = Field(description="Total matching records (not just this page)")
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    """Standard error body returned on failures."""

    detail: str
