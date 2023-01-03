"""empty message

Revision ID: b7207f2c7868
Revises: 72b9a59181b5
Create Date: 2022-11-19 15:13:43.669804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7207f2c7868'
down_revision = '72b9a59181b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('books_users_user_id_fkey', 'books_users', type_='foreignkey')
    op.drop_constraint('books_users_book_id_fkey', 'books_users', type_='foreignkey')
    op.create_foreign_key(None, 'books_users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'books_users', 'books', ['book_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books_users', type_='foreignkey')
    op.drop_constraint(None, 'books_users', type_='foreignkey')
    op.create_foreign_key('books_users_book_id_fkey', 'books_users', 'books', ['book_id'], ['id'])
    op.create_foreign_key('books_users_user_id_fkey', 'books_users', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
