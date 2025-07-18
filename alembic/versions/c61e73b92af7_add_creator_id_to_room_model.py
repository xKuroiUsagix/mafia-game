"""add creator_id to room model

Revision ID: c61e73b92af7
Revises: cd91fb1ff12c
Create Date: 2025-07-03 16:06:55.829750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c61e73b92af7'
down_revision: Union[str, Sequence[str], None] = 'cd91fb1ff12c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('creator_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'rooms', 'users', ['creator_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.drop_column('rooms', 'creator_id')
    # ### end Alembic commands ###
