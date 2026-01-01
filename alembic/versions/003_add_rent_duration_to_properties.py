"""Add rent_duration column to properties table.

Revision ID: 003
Revises: 002
Create Date: 2026-01-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the rent_duration column to properties table
    op.add_column("properties", sa.Column("rent_duration", sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the rent_duration column from properties table
    op.drop_column("properties", "rent_duration")
