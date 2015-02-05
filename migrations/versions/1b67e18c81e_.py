"""Create show table.

Revision ID: 1b67e18c81e
Revises: None
Create Date: 2015-02-05 13:42:01.673717

"""

from alembic import op
import sqlalchemy as sa


revision = '1b67e18c81e'
down_revision = None


def upgrade():
    op.create_table(
        'show',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('feed_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('latest_episode_date', sa.Date(), nullable=True),
        sa.Column('next_episode_date', sa.Date(), nullable=True),
        sa.Column('is_ended', sa.Boolean(), nullable=True),

        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_show_feed_id'), 'show', ['feed_id'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_show_feed_id'), table_name='show')
    op.drop_table('show')
