"""updated active code field in users

Revision ID: 3d1d2f75f290
Revises: 7077672d851a
Create Date: 2024-03-24 10:06:24.642471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d1d2f75f290'
down_revision: Union[str, None] = '7077672d851a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('ref_code_is_active', sa.Boolean(), nullable=True))
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.BOOLEAN(), nullable=True))
    op.drop_column('users', 'ref_code_is_active')
    # ### end Alembic commands ###
