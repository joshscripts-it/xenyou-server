"""Add pet_owner column to properties table.

Revision ID: 001
Revises: 
Create Date: 2026-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the pet_owner column to properties table
    op.add_column('properties', sa.Column('pet_owner', sa.Boolean(), nullable=True))


def downgrade() -> None:
    # Remove the pet_owner column from properties table
    op.drop_column('properties', 'pet_owner')
