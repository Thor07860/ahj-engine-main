"""sync_schema_with_models

Revision ID: 427cf298b538
Revises: 003_add_ahj_columns
Create Date: 2026-03-02 13:25:44.737808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '427cf298b538'
down_revision: Union[str, Sequence[str], None] = '003_add_ahj_columns'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = inspect(conn)

    table_columns = {
        table_name: {column["name"] for column in inspector.get_columns(table_name)}
        for table_name in ["states", "combination_mapper", "notes"]
    }

    if "country_id" not in table_columns["states"]:
        op.add_column("states", sa.Column("country_id", sa.Integer(), nullable=True))

    if "created_at" not in table_columns["combination_mapper"]:
        op.add_column(
            "combination_mapper",
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
        )

    if "created_at" not in table_columns["notes"]:
        op.add_column(
            "notes",
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
        )

    existing_fks = inspector.get_foreign_keys("states")
    fk_exists = any(
        fk.get("referred_table") == "countries"
        and fk.get("constrained_columns") == ["country_id"]
        for fk in existing_fks
    )
    if "country_id" in {column["name"] for column in inspector.get_columns("states")} and not fk_exists:
        op.create_foreign_key(
            "fk_states_country_id_countries",
            "states",
            "countries",
            ["country_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
