"""
Employee ORM model.

Maps to the `employees` table in MySQL. Indexes are chosen to support
the primary search use-case (name and department prefix/substring matching).

Index strategy:
- ix_employees_name: B-tree index on `name`. Efficient for prefix searches
  (WHERE name LIKE 'rahul%'). For substring searches (LIKE '%rahul%'), MySQL
  cannot use the index for range scans, but the index still helps if the table
  is large and the query planner chooses an index scan. For the expected dataset
  size (thousands to low tens-of-thousands), a full-table scan with LIKE is
  acceptable. For larger datasets, consider MySQL FULLTEXT indexes.
- ix_employees_department: B-tree index on `department`. Same trade-offs apply.
"""

from datetime import date

from sqlalchemy import Date, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    designation: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_joining: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        Index("ix_employees_name", "name"),
        Index("ix_employees_department", "department"),
    )

    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, name={self.name!r}, department={self.department!r})>"
