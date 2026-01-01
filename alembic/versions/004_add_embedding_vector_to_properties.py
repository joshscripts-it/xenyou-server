"""Add embedding_vector column to properties table.

Revision ID: 004
Revises: 003
Create Date: 2026-01-01 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the embedding_vector column to properties table
    op.add_column("properties", sa.Column("embedding_vector", JSON(), nullable=True))


def downgrade() -> None:
    # Remove the embedding_vector column from properties table
    op.drop_column("properties", "embedding_vector")
