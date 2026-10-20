"""
Employee repository – owns all database query logic.

Design:
- All queries use parameterized SQLAlchemy expressions (no string concatenation).
- Search uses case-insensitive LIKE with '%term%' for substring matching.
  This is the most usable mode for an internal directory (users expect "rah"
  to match "Rahul" anywhere in the name).
- Pagination uses LIMIT/OFFSET with a deterministic ORDER BY id to guarantee
  stable page ordering.
- The total count query runs a SELECT COUNT(*) with the same filters so the
  frontend can display accurate pagination metadata.

Performance notes (documented in README):
- B-tree indexes on name/department help with prefix patterns but MySQL cannot
  use them for leading-wildcard LIKE ('%term%'). For the expected dataset size
  of an internal company directory (< 50k rows), this is acceptable.
- For larger datasets, FULLTEXT indexes or an external search engine would be
  appropriate. This is not added here because the assignment specifies MySQL
  and a simple directory tool.
"""

import logging
from typing import List, Tuple

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.employee import Employee

logger = logging.getLogger(__name__)


class EmployeeRepository:
    """Data-access layer for employee queries."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def search(
        self,
        search_term: str = "",
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[Employee], int]:
        """
        Search employees by name or department.

        Returns a tuple of (matching employees for this page, total match count).
        """
        query = self._db.query(Employee)

        if search_term:
            # Case-insensitive substring search across name and department.
            # MySQL's default utf8mb4_0900_ai_ci collation is already
            # case-insensitive, but we use lower() for portability with
            # other collations or test databases (SQLite).
            pattern = f"%{search_term.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Employee.name).like(pattern),
                    func.lower(Employee.department).like(pattern),
                )
            )

        # Total count for the filtered set (before pagination)
        total = query.count()

        # Deterministic ordering for stable pagination
        employees = (
            query
            .order_by(Employee.id)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return employees, total
