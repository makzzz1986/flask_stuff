"""empty message

Revision ID: fa8d7daac7fb
Revises: 
Create Date: 2018-01-29 16:16:37.695557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa8d7daac7fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('azs_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('azstype', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('divisions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('div_name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dzo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('service', sa.String(length=60), nullable=True),
    sa.Column('manager', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('models_gate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_models_gate_name'), 'models_gate', ['name'], unique=False)
    op.create_table('models_router',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_models_router_name'), 'models_router', ['name'], unique=False)
    op.create_table('prereasons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reason_name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reasons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reason_name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('region_mgmt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ru',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('geo', sa.String(length=60), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('division', sa.Integer(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['division'], ['divisions.id'], ),
    sa.ForeignKeyConstraint(['rank'], ['rank.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('azs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sixdign', sa.String(length=6), nullable=True),
    sa.Column('ru', sa.Integer(), nullable=True),
    sa.Column('region_mgmt', sa.Integer(), nullable=True),
    sa.Column('num', sa.Integer(), nullable=True),
    sa.Column('hostname', sa.String(length=30), nullable=True),
    sa.Column('dzo', sa.Integer(), nullable=True),
    sa.Column('azs_type', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('data_added', sa.DateTime(), nullable=True),
    sa.Column('user_added', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('mss_ip', sa.String(length=15), nullable=True),
    sa.Column('just_added', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['azs_type'], ['azs_type.id'], ),
    sa.ForeignKeyConstraint(['dzo'], ['dzo.id'], ),
    sa.ForeignKeyConstraint(['region_mgmt'], ['region_mgmt.id'], ),
    sa.ForeignKeyConstraint(['ru'], ['ru.id'], ),
    sa.ForeignKeyConstraint(['user_added'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_azs_sixdign'), 'azs', ['sixdign'], unique=True)
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=200), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_timestamp'), 'comment', ['timestamp'], unique=False)
    op.create_table('hardware',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gate_model', sa.Integer(), nullable=True),
    sa.Column('gate_serial', sa.String(length=10), nullable=True),
    sa.Column('gate_lic', sa.String(length=10), nullable=True),
    sa.Column('gate_install', sa.DateTime(), nullable=True),
    sa.Column('router_model', sa.Integer(), nullable=True),
    sa.Column('router_serial', sa.String(length=10), nullable=True),
    sa.Column('router_install', sa.DateTime(), nullable=True),
    sa.Column('azs_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['azs_id'], ['azs.id'], ),
    sa.ForeignKeyConstraint(['gate_model'], ['models_gate.id'], ),
    sa.ForeignKeyConstraint(['router_model'], ['models_router.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gate_serial'),
    sa.UniqueConstraint('router_serial')
    )
    op.create_table('ip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('interface', sa.String(length=10), nullable=True),
    sa.Column('net', sa.String(length=35), nullable=True),
    sa.Column('description', sa.String(length=30), nullable=True),
    sa.Column('renew_last_time', sa.DateTime(), nullable=True),
    sa.Column('azs_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azs_id'], ['azs.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('net')
    )
    op.create_table('status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('reason', sa.Integer(), nullable=True),
    sa.Column('added', sa.DateTime(), nullable=True),
    sa.Column('prereason', sa.Integer(), nullable=True),
    sa.Column('preadded', sa.DateTime(), nullable=True),
    sa.Column('azs_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['azs_id'], ['azs.id'], ),
    sa.ForeignKeyConstraint(['prereason'], ['prereasons.id'], ),
    sa.ForeignKeyConstraint(['reason'], ['reasons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status')
    op.drop_table('ip')
    op.drop_table('hardware')
    op.drop_index(op.f('ix_comment_timestamp'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_azs_sixdign'), table_name='azs')
    op.drop_table('azs')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('ru')
    op.drop_table('region_mgmt')
    op.drop_table('reasons')
    op.drop_table('rank')
    op.drop_table('prereasons')
    op.drop_index(op.f('ix_models_router_name'), table_name='models_router')
    op.drop_table('models_router')
    op.drop_index(op.f('ix_models_gate_name'), table_name='models_gate')
    op.drop_table('models_gate')
    op.drop_table('dzo')
    op.drop_table('divisions')
    op.drop_table('azs_type')
    # ### end Alembic commands ###