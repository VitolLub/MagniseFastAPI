"""New Migration

Revision ID: 608e42f1a574
Revises: 76225fcf8768
Create Date: 2021-09-29 11:32:19.860151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '608e42f1a574'
down_revision = '76225fcf8768'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
