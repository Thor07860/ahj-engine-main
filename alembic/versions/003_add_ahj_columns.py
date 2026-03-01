"""Add missing AHJ columns to ahjs table

Revision ID: 003_add_ahj_columns
Revises: 002_add_label_columns
Create Date: 2026-03-01 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '003_add_ahj_columns'
down_revision = '002_add_label_columns'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add missing columns to ahjs table if they don't exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [c['name'] for c in inspector.get_columns('ahjs')]
    
    if 'name' not in existing_columns:
        op.add_column('ahjs', sa.Column('name', sa.String(255), nullable=False, server_default=''))
    
    if 'ahj_name' not in existing_columns:
        op.add_column('ahjs', sa.Column('ahj_name', sa.String(255), nullable=True))
    
    if 'state_id' not in existing_columns:
        op.add_column('ahjs', sa.Column('state_id', sa.Integer(), nullable=False, server_default='0'))
    
    if 'county' not in existing_columns:
        op.add_column('ahjs', sa.Column('county', sa.String(255), nullable=True))
    
    if 'city' not in existing_columns:
        op.add_column('ahjs', sa.Column('city', sa.String(255), nullable=True))
    
    if 'guidelines' not in existing_columns:
        op.add_column('ahjs', sa.Column('guidelines', sa.Text(), nullable=True))
    
    if 'fireset_back' not in existing_columns:
        op.add_column('ahjs', sa.Column('fireset_back', sa.Float(), nullable=True))
    
    if 'jurisdiction_type' not in existing_columns:
        op.add_column('ahjs', sa.Column('jurisdiction_type', sa.String(100), nullable=True))
    
    if 'phone' not in existing_columns:
        op.add_column('ahjs', sa.Column('phone', sa.String(50), nullable=True))
    
    if 'email' not in existing_columns:
        op.add_column('ahjs', sa.Column('email', sa.String(255), nullable=True))
    
    if 'website' not in existing_columns:
        op.add_column('ahjs', sa.Column('website', sa.String(500), nullable=True))
    
    if 'created_at' not in existing_columns:
        op.add_column('ahjs', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()))


def downgrade() -> None:
    pass
