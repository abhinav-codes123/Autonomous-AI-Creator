"""Add is_active column to agents table."""

from alembic import op
import sqlalchemy as sa


revision = "004_add_is_active_to_agents"
down_revision = "003_make_topic_urls_agent_scoped"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    columns = {col["name"] for col in sa.inspect(bind).get_columns("agents")}
    if "is_active" not in columns:
        op.add_column("agents", sa.Column("is_active", sa.Boolean(), nullable=False, server_default="1"))


def downgrade() -> None:
    bind = op.get_bind()
    columns = {col["name"] for col in sa.inspect(bind).get_columns("agents")}
    if "is_active" in columns:
        op.drop_column("agents", "is_active")
