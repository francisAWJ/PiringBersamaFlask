"""empty message

Revision ID: 05d491b582e3
Revises: 7fecb8bed8df
Create Date: 2024-12-16 11:04:24.761879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05d491b582e3'
down_revision = '7fecb8bed8df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=30),
               nullable=False)

    # ### end Alembic commands ###
