"""empty message

Revision ID: d83a16f702fc
Revises: 1138ab9a0272
Create Date: 2021-04-12 17:24:24.460634

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd83a16f702fc'
down_revision = '1138ab9a0272'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=False))
    op.drop_column('shows', 'ShowDate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('ShowDate', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('shows', 'start_time')
    # ### end Alembic commands ###
