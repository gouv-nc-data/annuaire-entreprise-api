"""clé étrangere nullable

Revision ID: a3c5d4fb38e4
Revises: 2b66a33c4bc4
Create Date: 2024-10-30 15:15:18.290951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c5d4fb38e4'
down_revision: Union[str, None] = '2b66a33c4bc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bilan', 'entreprise_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('bilan', 'etablissement_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('dirigeant', 'entreprise_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('dirigeant', 'etablissement_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('indicateurs_financiers', 'entreprise_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('indicateurs_financiers', 'etablissement_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('indicateurs_financiers', 'etablissement_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('indicateurs_financiers', 'entreprise_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('dirigeant', 'etablissement_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('dirigeant', 'entreprise_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bilan', 'etablissement_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('bilan', 'entreprise_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
