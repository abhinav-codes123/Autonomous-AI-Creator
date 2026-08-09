"""Initial schema migration for Agents, Topics, RejectedTopics, Posts, and PostSources

Revision ID: 001_initial_migration
Revises: 
Create Date: 2026-08-08 02:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_migration'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'agents',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'topics',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('agent_id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('url', sa.String(length=2048), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('discovered_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
        ,sa.UniqueConstraint('agent_id', 'url', name='uq_agent_topic_url')
    )
    op.create_index(op.f('ix_topics_agent_id'), 'topics', ['agent_id'], unique=False)
    op.create_index(op.f('ix_topics_url'), 'topics', ['url'], unique=False)

    op.create_table(
        'rejected_topics',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('topic_id', sa.Uuid(), nullable=False),
        sa.Column('reason', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['topic_id'], ['topics.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('topic_id')
    )

    op.create_table(
        'posts',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('agent_id', sa.Uuid(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('rationale', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['agent_id'], ['agents.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_agent_id'), 'posts', ['agent_id'], unique=False)

    op.create_table(
        'post_sources',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('post_id', sa.Uuid(), nullable=False),
        sa.Column('url', sa.String(length=2048), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_sources_post_id'), 'post_sources', ['post_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_post_sources_post_id'), table_name='post_sources')
    op.drop_table('post_sources')
    op.drop_index(op.f('ix_posts_agent_id'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('rejected_topics')
    op.drop_index(op.f('ix_topics_url'), table_name='topics')
    op.drop_index(op.f('ix_topics_agent_id'), table_name='topics')
    op.drop_table('topics')
    op.drop_table('agents')
