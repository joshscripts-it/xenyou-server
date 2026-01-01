"""Add move_in_date column to properties table.

Revision ID: 002
Revises: 001
Create Date: 2026-01-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the move_in_date column to properties table
    op.add_column("properties", sa.Column("move_in_date", sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove the move_in_date column from properties table
    op.drop_column("properties", "move_in_date")
