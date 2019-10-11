"""empty message

Revision ID: 1614170b5606
Revises: 135f03c47175
Create Date: 2019-10-10 20:14:19.315289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1614170b5606'
down_revision = '135f03c47175'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###