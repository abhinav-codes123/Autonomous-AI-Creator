"""Post Repository for database access."""

import uuid
from typing import Sequence
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.models.post_source import PostSource


class PostRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_post(
        self,
        agent_id: uuid.UUID,
        text: str,
        rationale: str,
        sources: list[str],
    ) -> Post:
        post = Post(
            id=uuid.uuid4(),
            agent_id=agent_id,
            text=text,
            rationale=rationale,
        )
        self.session.add(post)
        await self.session.flush()

        for source_url in sources:
            source = PostSource(
                id=uuid.uuid4(),
                post_id=post.id,
                url=source_url,
            )
            self.session.add(source)

        await self.session.commit()
        await self.session.refresh(post, ["sources"])
        return post

    async def get_posts_by_agent(
        self,
        agent_id: uuid.UUID,
        limit: int = 100,
    ) -> Sequence[Post]:
        stmt = (
            select(Post)
            .where(Post.agent_id == agent_id)
            .options(selectinload(Post.sources))
            .order_by(Post.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_recent_posts(self, limit: int = 100) -> Sequence[Post]:
        stmt = (
            select(Post)
            .options(selectinload(Post.sources))
            .order_by(Post.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_recent_posts_by_agent(self, agent_id: uuid.UUID, limit: int = 100) -> Sequence[Post]:
        stmt = (
            select(Post)
            .where(Post.agent_id == agent_id)
            .options(selectinload(Post.sources))
            .order_by(Post.created_at.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count_posts_by_agent(self, agent_id: uuid.UUID) -> int:
        stmt = select(func.count(Post.id)).where(Post.agent_id == agent_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0
