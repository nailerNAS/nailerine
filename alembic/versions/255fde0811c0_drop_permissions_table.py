"""drop permissions table

Revision ID: 255fde0811c0
Revises: 
Create Date: 2019-08-05 10:38:33.546320

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '255fde0811c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('permissions')


def downgrade():
    op.create_table('permissions',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('user_id', sa.Integer, nullable=False),
                    sa.Column('allow', sa.Boolean, nullable=False),
                    sa.Column('date', sa.DateTime))
