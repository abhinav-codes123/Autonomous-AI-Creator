"""Scope legacy topics to the agent that published or evaluated them.

Revision ID: 002_scope_topics_to_agents
Revises: 001_initial_migration
"""

from alembic import op
import sqlalchemy as sa


revision = "002_scope_topics_to_agents"
down_revision = "001_initial_migration"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Migrate the old global-topic development schema when it is unambiguous."""
    bind = op.get_bind()
    columns = {column["name"] for column in sa.inspect(bind).get_columns("topics")}
    if "agent_id" in columns:
        return

    agents = bind.execute(sa.text("SELECT id FROM agents ORDER BY created_at")).fetchall()
    topic_count = bind.execute(sa.text("SELECT COUNT(*) FROM topics")).scalar_one()
    if topic_count and not agents:
        raise RuntimeError(
            "Cannot scope legacy topics because the database has no agents. "
            "Run scripts/reset_database.py for a development reset."
        )

    op.add_column("topics", sa.Column("agent_id", sa.Uuid(), nullable=True))
    if topic_count:
        # Published topics can be assigned precisely using their persisted post
        # sources. The legacy topics table did not contain an agent ID.
        bind.execute(
            sa.text(
                "UPDATE topics SET agent_id = ("
                "SELECT posts.agent_id FROM posts "
                "JOIN post_sources ON post_sources.post_id = posts.id "
                "WHERE post_sources.url = topics.url LIMIT 1"
                ") WHERE EXISTS ("
                "SELECT 1 FROM posts JOIN post_sources ON post_sources.post_id = posts.id "
                "WHERE post_sources.url = topics.url"
                ")"
            )
        )
        # Discovery-only and rejected legacy rows never count as publishing
        # memory. Give those orphan rows a stable owner solely to satisfy the
        # new non-null, agent-scoped schema.
        bind.execute(
            sa.text("UPDATE topics SET agent_id = :agent_id WHERE agent_id IS NULL"),
            {"agent_id": agents[0].id},
        )

    with op.batch_alter_table("topics") as batch_op:
        batch_op.alter_column("agent_id", nullable=False)
        batch_op.create_foreign_key("fk_topics_agent_id_agents", "agents", ["agent_id"], ["id"], ondelete="CASCADE")
        batch_op.create_unique_constraint("uq_agent_topic_url", ["agent_id", "url"])
    op.create_index("ix_topics_agent_id", "topics", ["agent_id"], unique=False)


def downgrade() -> None:
    # Dropping agent ownership would reintroduce unsafe global publishing memory.
    raise RuntimeError("This migration is intentionally irreversible.")
