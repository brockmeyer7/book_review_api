"""empty message

Revision ID: 455bd782ef1b
Revises: 7a476ff97e71
Create Date: 2022-11-06 13:09:38.925754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '455bd782ef1b'
down_revision = '7a476ff97e71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books_awards',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('award_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['award_id'], ['awards.id'], ),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('book_id', 'award_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books_awards')
    # ### end Alembic commands ###
