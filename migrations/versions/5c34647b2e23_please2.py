"""please2

Revision ID: 5c34647b2e23
Revises: 91318b9d2197
Create Date: 2023-03-31 17:02:12.209441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c34647b2e23'
down_revision = '91318b9d2197'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('owner', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_board_create_datetime'), 'board', ['create_datetime'], unique=False)
    op.create_index(op.f('ix_board_owner'), 'board', ['owner'], unique=False)
    op.create_table('board_article',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('board_id', sa.BigInteger(), nullable=False),
    sa.Column('owner', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.String(length=255), nullable=True),
    sa.Column('create_datetime', sa.DateTime(), nullable=True),
    sa.Column('last_update_datetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_board_article_board_id'), 'board_article', ['board_id'], unique=False)
    op.create_index(op.f('ix_board_article_create_datetime'), 'board_article', ['create_datetime'], unique=False)
    op.create_index(op.f('ix_board_article_owner'), 'board_article', ['owner'], unique=False)
    op.create_index(op.f('ix_board_article_title'), 'board_article', ['title'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('fullname', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_board_article_title'), table_name='board_article')
    op.drop_index(op.f('ix_board_article_owner'), table_name='board_article')
    op.drop_index(op.f('ix_board_article_create_datetime'), table_name='board_article')
    op.drop_index(op.f('ix_board_article_board_id'), table_name='board_article')
    op.drop_table('board_article')
    op.drop_index(op.f('ix_board_owner'), table_name='board')
    op.drop_index(op.f('ix_board_create_datetime'), table_name='board')
    op.drop_table('board')
    # ### end Alembic commands ###