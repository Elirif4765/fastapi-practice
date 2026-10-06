"""add last few columns to posts table

Revision ID: f0fb298e8b1c
Revises: 19a912c43a8c
Create Date: 2026-10-06 13:56:18.030482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0fb298e8b1c'
down_revision = '19a912c43a8c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
