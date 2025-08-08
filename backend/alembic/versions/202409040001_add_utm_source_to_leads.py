"""add utm_source to leads

Revision ID: 202409040001
Revises: 
Create Date: 2024-09-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '202409040001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('leads', sa.Column('utm_source', sa.String(length=128), nullable=True))


def downgrade() -> None:
    op.drop_column('leads', 'utm_source')
