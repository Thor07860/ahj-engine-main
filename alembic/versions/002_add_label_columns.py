"""Add label columns to labels table

Revision ID: 002_add_label_columns
Revises: None
Create Date: 2026-03-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '002_add_label_columns'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns to labels table if they don't exist
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [c['name'] for c in inspector.get_columns('labels')]
    
    if 'upc_code' not in existing_columns:
        op.add_column('labels', sa.Column('upc_code', sa.String(100), nullable=True, unique=True))
    
    if 'label_number' not in existing_columns:
        op.add_column('labels', sa.Column('label_number', sa.String(100), nullable=True))
    
    if 'label_name' not in existing_columns:
        op.add_column('labels', sa.Column('label_name', sa.Text(), nullable=True))
    
    if 'length' not in existing_columns:
        op.add_column('labels', sa.Column('length', sa.String(50), nullable=True))
    
    if 'width' not in existing_columns:
        op.add_column('labels', sa.Column('width', sa.String(50), nullable=True))
    
    if 'image_url' not in existing_columns:
        op.add_column('labels', sa.Column('image_url', sa.String(500), nullable=True))
    
    if 'background_color' not in existing_columns:
        op.add_column('labels', sa.Column('background_color', sa.String(100), nullable=True))
    
    if 'text_color' not in existing_columns:
        op.add_column('labels', sa.Column('text_color', sa.String(100), nullable=True))


def downgrade() -> None:
    pass
