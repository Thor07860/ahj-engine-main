"""add_missing_created_at_columns

Revision ID: 424c7ee2edd2
Revises: 427cf298b538
Create Date: 2026-03-02 13:28:42.675916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '424c7ee2edd2'
down_revision: Union[str, Sequence[str], None] = '427cf298b538'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)

    targets = ["ahj_codes", "categories", "countries", "equipment", "state_codes"]
    for table_name in targets:
        existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
        if "created_at" not in existing_columns:
            op.add_column(
                table_name,
                sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
            )


def downgrade() -> None:
    """Downgrade schema."""
    pass
