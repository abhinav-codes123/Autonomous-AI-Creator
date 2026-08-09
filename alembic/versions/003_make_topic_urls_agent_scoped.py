"""Replace the legacy global topic URL uniqueness with agent-scoped uniqueness."""

from alembic import op
import sqlalchemy as sa


revision = "003_make_topic_urls_agent_scoped"
down_revision = "002_scope_topics_to_agents"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    indexes = {index["name"]: index for index in sa.inspect(bind).get_indexes("topics")}
    legacy_url_index = indexes.get("ix_topics_url")
    if legacy_url_index and legacy_url_index.get("unique"):
        op.drop_index("ix_topics_url", table_name="topics")
        op.create_index("ix_topics_url", "topics", ["url"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    indexes = {index["name"]: index for index in sa.inspect(bind).get_indexes("topics")}
    if "ix_topics_url" in indexes:
        op.drop_index("ix_topics_url", table_name="topics")
    op.create_index("ix_topics_url", "topics", ["url"], unique=True)
