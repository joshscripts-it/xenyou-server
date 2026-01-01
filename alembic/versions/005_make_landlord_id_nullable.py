"""Make landlord_id nullable in properties table.

Revision ID: 005
Revises: 004
Create Date: 2026-01-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Alter landlord_id to be nullable
    op.alter_column(
        "properties",
        "landlord_id",
        existing_type=postgresql.UUID(),
        nullable=True,
    )


def downgrade() -> None:
    # Revert landlord_id to NOT NULL
    op.alter_column(
        "properties",
        "landlord_id",
        existing_type=postgresql.UUID(),
        nullable=False,
    )
