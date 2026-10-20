"""create employees table

Revision ID: 0001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("department", sa.String(length=100), nullable=False),
        sa.Column("designation", sa.String(length=100), nullable=False),
        sa.Column("date_of_joining", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_employees_name", "employees", ["name"])
    op.create_index("ix_employees_department", "employees", ["department"])


def downgrade() -> None:
    op.drop_index("ix_employees_department", table_name="employees")
    op.drop_index("ix_employees_name", table_name="employees")
    op.drop_table("employees")
