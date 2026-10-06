"""add foreign-key to posts table

Revision ID: 19a912c43a8c
Revises: 6b43e7ff8863
Create Date: 2026-10-06 13:46:05.264106

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19a912c43a8c'
down_revision = '6b43e7ff8863'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', "owner_id")
