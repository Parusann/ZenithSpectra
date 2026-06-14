"""add content_items.search_vector generated tsvector + GIN index

Revision ID: a1b2c3d4e5f6
Revises: 6d6e10f2abd1
Create Date: 2026-06-14

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '6d6e10f2abd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # DB-generated tsvector over title + cleaned_content, indexed with GIN so
    # full-text search uses the index instead of recomputing to_tsvector per row.
    op.execute(
        "ALTER TABLE content_items ADD COLUMN IF NOT EXISTS search_vector tsvector "
        "GENERATED ALWAYS AS ("
        "to_tsvector('english', coalesce(title, '') || ' ' || coalesce(cleaned_content, ''))"
        ") STORED"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_content_items_search_vector "
        "ON content_items USING gin (search_vector)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_content_items_search_vector")
    op.execute("ALTER TABLE content_items DROP COLUMN IF EXISTS search_vector")
