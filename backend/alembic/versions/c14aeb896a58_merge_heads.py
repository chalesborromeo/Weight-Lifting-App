"""merge_heads

Revision ID: c14aeb896a58
Revises: 1e960f0e451a, f20abfdcef50
Create Date: 2026-05-02 20:35:37.772093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c14aeb896a58'
down_revision: Union[str, Sequence[str], None] = ('1e960f0e451a', 'f20abfdcef50')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
