"""empty message

Revision ID: a8bdffcb337a
Revises: 997bfdfc043a
Create Date: 2022-11-06 13:16:50.137156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8bdffcb337a'
down_revision = '997bfdfc043a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'reading_challenges', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reading_challenges', type_='foreignkey')
    # ### end Alembic commands ###
