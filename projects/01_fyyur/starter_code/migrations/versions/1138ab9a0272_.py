"""empty message

Revision ID: 1138ab9a0272
Revises: 72c92c43d91b
Create Date: 2021-04-06 15:37:36.951891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1138ab9a0272'
down_revision = '72c92c43d91b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.execute('UPDATE "Venue" SET seeking_talent = false WHERE seeking_talent IS NULL')

    op.alter_column('Venue', 'seeking_talent', nullable=False)            
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'website_link')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
