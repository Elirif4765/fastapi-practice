"""create posts table

Revision ID: 392fe920bbeb
Revises: 
Create Date: 2026-10-06 12:54:18.530027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '392fe920bbeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
