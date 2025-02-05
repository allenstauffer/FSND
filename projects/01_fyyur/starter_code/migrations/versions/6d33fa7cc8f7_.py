"""empty message

Revision ID: 6d33fa7cc8f7
Revises: 78168b7372f2
Create Date: 2021-04-15 20:29:55.906505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d33fa7cc8f7'
down_revision = '78168b7372f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.execute("UPDATE artist SET genres = '{}' WHERE genres IS NULL")
    op.execute("UPDATE venue SET genres = '{}' WHERE genres IS NULL")

    op.alter_column('artist', 'genres', nullable=False)    
    op.alter_column('venue', 'genres', nullable=False)    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'genres')
    # ### end Alembic commands ###
