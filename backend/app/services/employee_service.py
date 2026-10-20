"""
Employee service – application-level business logic.

Sits between routers and repository. Currently thin because the search
use-case is straightforward, but this layer is where validation rules,
caching, or cross-cutting concerns (audit logging, rate limiting) would live
when the application grows.
"""

import logging

from sqlalchemy.orm import Session

from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeResponse, PaginatedResponse

logger = logging.getLogger(__name__)


class EmployeeService:
    """Coordinates employee search operations."""

    def __init__(self, db: Session) -> None:
        self._repository = EmployeeRepository(db)

    def search_employees(
        self,
        search_term: str = "",
        limit: int = 20,
        offset: int = 0,
    ) -> PaginatedResponse[EmployeeResponse]:
        """
        Search employees and return a paginated response.

        Delegates filtering/pagination to the repository and maps
        ORM models to response schemas.
        """
        employees, total = self._repository.search(
            search_term=search_term,
            limit=limit,
            offset=offset,
        )

        items = [EmployeeResponse.model_validate(emp) for emp in employees]

        return PaginatedResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset,
        )
