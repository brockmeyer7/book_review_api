"""empty message

Revision ID: fc74d2f11992
Revises: bb94d2bbb7f1
Create Date: 2022-11-13 15:09:43.077727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc74d2f11992'
down_revision = 'bb94d2bbb7f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'reading_challenges', ['user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reading_challenges', type_='unique')
    # ### end Alembic commands ###