"""empty message

Revision ID: 135f03c47175
Revises: 
Create Date: 2019-10-10 19:04:49.636470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135f03c47175'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('sample',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('composition', sa.String(length=100), nullable=True),
    sa.Column('fab_method', sa.String(length=100), nullable=True),
    sa.Column('fab_date', sa.String(length=10), nullable=True),
    sa.Column('notes', sa.String(length=200), nullable=True),
    sa.Column('experiments', sa.PickleType(), nullable=True),
    sa.Column('ispublic', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sample_composition'), 'sample', ['composition'], unique=False)
    op.create_index(op.f('ix_sample_experiments'), 'sample', ['experiments'], unique=False)
    op.create_index(op.f('ix_sample_fab_date'), 'sample', ['fab_date'], unique=False)
    op.create_index(op.f('ix_sample_fab_method'), 'sample', ['fab_method'], unique=False)
    op.create_index(op.f('ix_sample_ispublic'), 'sample', ['ispublic'], unique=False)
    op.create_index(op.f('ix_sample_name'), 'sample', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sample_name'), table_name='sample')
    op.drop_index(op.f('ix_sample_ispublic'), table_name='sample')
    op.drop_index(op.f('ix_sample_fab_method'), table_name='sample')
    op.drop_index(op.f('ix_sample_fab_date'), table_name='sample')
    op.drop_index(op.f('ix_sample_experiments'), table_name='sample')
    op.drop_index(op.f('ix_sample_composition'), table_name='sample')
    op.drop_table('sample')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
