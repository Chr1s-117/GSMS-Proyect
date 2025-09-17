"""agregar tabla usuarios

Revision ID: 97e302027765
Revises: ac170839499f
Create Date: 2025-08-31 22:46:32.802173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97e302027765'
down_revision: Union[str, Sequence[str], None] = 'ac170839499f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
