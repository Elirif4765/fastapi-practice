"""add content column to posts table

Revision ID: ce8ece0dd15c
Revises: 392fe920bbeb
Create Date: 2026-10-06 13:12:48.935727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce8ece0dd15c'
down_revision = '392fe920bbeb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
