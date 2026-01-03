"""add is_admin

Revision ID: 46ffd3560590
Revises: ad03a6568be7
Create Date: 2026-01-02 20:56:30.823994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '46ffd3560590'
down_revision: Union[str, Sequence[str], None] = 'ad03a6568be7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('users', 'user')
    op.drop_index('ix_users_email', table_name='user')
    op.drop_index('ix_users_id', table_name='user')
    op.drop_index('ix_users_phone_number', table_name='user')
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_phone_number'), 'user', ['phone_number'], unique=True)
    op.add_column('user', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))
    op.alter_column('user', 'is_active', nullable=False)
    op.alter_column('user', 'is_verified', nullable=False)
    op.alter_column('user', 'created_at', type_=sa.DateTime(timezone=True), nullable=False)
    op.alter_column('user', 'updated_at', type_=sa.DateTime(timezone=True), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('user', 'updated_at', type_=sa.DateTime(), nullable=True)
    op.alter_column('user', 'created_at', type_=sa.DateTime(), nullable=True)
    op.alter_column('user', 'is_verified', nullable=True)
    op.alter_column('user', 'is_active', nullable=True)
    op.drop_column('user', 'is_admin')
    op.drop_index(op.f('ix_user_phone_number'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.create_index('ix_users_phone_number', 'user', ['phone_number'], unique=True)
    op.create_index('ix_users_id', 'user', ['id'], unique=False)
    op.create_index('ix_users_email', 'user', ['email'], unique=True)
    op.rename_table('user', 'users')
