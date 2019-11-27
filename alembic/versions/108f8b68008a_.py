"""empty message

Revision ID: 108f8b68008a
Revises: 255fde0811c0
Create Date: 2019-08-23 10:25:44.169710

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '108f8b68008a'
down_revision = '255fde0811c0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('cached_messages',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column('chat_id', sa.Integer, nullable=False),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.Column('message_id', sa.Integer, nullable=False),
                    sa.Column('file_id', sa.String),
                    sa.Column('chat_name', sa.String),
                    sa.Column('user_name', sa.String),
                    sa.Column('text', sa.String))


def downgrade():
    op.drop_table('cached_messages')
