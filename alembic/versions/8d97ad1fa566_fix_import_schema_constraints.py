"""fix_import_schema_constraints

Revision ID: 8d97ad1fa566
Revises: 424c7ee2edd2
Create Date: 2026-03-02 13:35:59.220870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '8d97ad1fa566'
down_revision: Union[str, Sequence[str], None] = '424c7ee2edd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)

    mapper_columns = {column["name"]: column for column in inspector.get_columns("combination_mapper")}
    if "code_id" in mapper_columns and not mapper_columns["code_id"]["nullable"]:
        op.alter_column("combination_mapper", "code_id", existing_type=sa.Integer(), nullable=True)
    if "label_id" in mapper_columns and not mapper_columns["label_id"]["nullable"]:
        op.alter_column("combination_mapper", "label_id", existing_type=sa.Integer(), nullable=True)

    label_columns = {column["name"]: column for column in inspector.get_columns("labels")}
    if "length" in label_columns and not isinstance(label_columns["length"]["type"], sa.String):
        op.execute('ALTER TABLE labels ALTER COLUMN "length" TYPE VARCHAR(50) USING "length"::text')
    if "width" in label_columns and not isinstance(label_columns["width"]["type"], sa.String):
        op.execute('ALTER TABLE labels ALTER COLUMN "width" TYPE VARCHAR(50) USING "width"::text')


def downgrade() -> None:
    """Downgrade schema."""
    pass
