"""added datetime

Revision ID: f0d654c21a0b
Revises: ae03585ea795
Create Date: 2023-02-05 18:00:15.301596

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0d654c21a0b'
down_revision = 'ae03585ea795'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_joined', sa.DateTime(), nullable=True))
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.drop_column('date_joined')

    # ### end Alembic commands ###
