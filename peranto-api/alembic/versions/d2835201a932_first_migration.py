"""first migration

Revision ID: d2835201a932
Revises: 
Create Date: 2023-04-11 13:11:03.379123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2835201a932'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=True),
    sa.Column('surname', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=256), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photo_id'), 'photo', ['id'], unique=False)
    op.create_index(op.f('ix_photo_url'), 'photo', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_photo_url'), table_name='photo')
    op.drop_index(op.f('ix_photo_id'), table_name='photo')
    op.drop_table('photo')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###