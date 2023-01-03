"""empty message

Revision ID: c148b2dfc284
Revises: 5fea60647fab
Create Date: 2022-11-06 12:41:57.636417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c148b2dfc284'
down_revision = '5fea60647fab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ratings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('rating_date', sa.Date(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ratings')
    # ### end Alembic commands ###