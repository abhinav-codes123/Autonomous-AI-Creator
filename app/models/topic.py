"""Topic SQLAlchemy model."""

import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Enum, Float, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.rejected_topic import RejectedTopic


class TopicStatus(str, enum.Enum):
    NEW = "NEW"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"


class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (UniqueConstraint('agent_id', 'url', name='uq_agent_topic_url'),)

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    agent_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("agents.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True, default="")
    url: Mapped[str] = mapped_column(String(2048), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[TopicStatus] = mapped_column(
        Enum(TopicStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TopicStatus.NEW,
    )
    discovered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    rejected_info: Mapped["RejectedTopic | None"] = relationship(
        "RejectedTopic",
        back_populates="topic",
        uselist=False,
        cascade="all, delete-orphan",
    )
