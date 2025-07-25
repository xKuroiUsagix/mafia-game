"""fix field name

Revision ID: 961a24d1c62a
Revises: 4aa602093a57
Create Date: 2025-07-09 02:33:46.166520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '961a24d1c62a'
down_revision: Union[str, Sequence[str], None] = '4aa602093a57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rool_sets', sa.Column('allow_sheriff', sa.Boolean(), nullable=False, server_default=sa.text('true')))
    op.drop_column('rool_sets', 'allow_sherif')
    op.alter_column('rooms', 'type_',
               existing_type=postgresql.ENUM('PUBLIC', 'PRIVATE', name='roomtype'),
               type_=sa.String(length=32),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'type_',
               existing_type=sa.String(length=32),
               type_=postgresql.ENUM('PUBLIC', 'PRIVATE', name='roomtype'),
               existing_nullable=False)
    op.add_column('rool_sets', sa.Column('allow_sherif', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('rool_sets', 'allow_sheriff')
    # ### end Alembic commands ###
