"""empty message

Revision ID: fc7c86621b41
Revises: 8cf7442eaab4
Create Date: 2018-11-17 02:43:34.153391

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc7c86621b41'
down_revision = '8cf7442eaab4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('poin', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'poin')
    op.drop_column('user', 'about')
    # ### end Alembic commands ###