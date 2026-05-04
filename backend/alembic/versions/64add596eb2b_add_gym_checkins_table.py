"""add_gym_checkins_table

Revision ID: 64add596eb2b
Revises: a05a33665353
Create Date: 2026-05-02 21:26:32.613279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64add596eb2b'
down_revision: Union[str, Sequence[str], None] = 'a05a33665353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'gym_checkins',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('gym_name', sa.String(200), nullable=False),
        sa.Column('gym_address', sa.String(200), nullable=True),
        sa.Column('checked_in_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('gym_checkins')
