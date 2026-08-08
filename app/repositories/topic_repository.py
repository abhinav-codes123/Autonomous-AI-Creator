"""Topic Repository for database access."""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.topic import Topic, TopicStatus
from app.models.rejected_topic import RejectedTopic


class TopicRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_url(self, url: str) -> Topic | None:
        stmt = select(Topic).options(selectinload(Topic.rejected_info)).where(Topic.url == url)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        title: str,
        summary: str,
        url: str,
        score: float = 0.0,
        status: TopicStatus = TopicStatus.NEW,
    ) -> Topic:
        existing = await self.get_by_url(url)
        if existing:
            existing.title = title
            existing.summary = summary
            existing.score = score
            existing.status = status
            await self.session.commit()
            await self.session.refresh(existing)
            return existing

        topic = Topic(
            id=uuid.uuid4(),
            title=title,
            summary=summary,
            url=url,
            score=score,
            status=status,
        )
        self.session.add(topic)
        await self.session.commit()
        await self.session.refresh(topic)
        return topic

    async def mark_rejected(self, topic: Topic, reason: str) -> RejectedTopic:
        topic.status = TopicStatus.REJECTED

        # Check if RejectedTopic record already exists
        stmt = select(RejectedTopic).where(RejectedTopic.topic_id == topic.id)
        result = await self.session.execute(stmt)
        existing_rejected = result.scalar_one_or_none()

        if existing_rejected:
            existing_rejected.reason = reason
            await self.session.commit()
            await self.session.refresh(existing_rejected)
            return existing_rejected

        rejected = RejectedTopic(
            id=uuid.uuid4(),
            topic_id=topic.id,
            reason=reason,
        )
        self.session.add(rejected)
        await self.session.commit()
        await self.session.refresh(rejected)
        return rejected

    async def mark_published(self, topic: Topic) -> Topic:
        topic.status = TopicStatus.PUBLISHED
        await self.session.commit()
        await self.session.refresh(topic)
        return topic

    async def list_recent_topics(self, limit: int = 100) -> Sequence[Topic]:
        stmt = select(Topic).order_by(Topic.discovered_at.desc()).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()
