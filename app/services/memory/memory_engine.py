"""Memory Engine for checking historical posts, covered topics, and deduplication."""

from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.topic import TopicStatus
from app.repositories.post_repository import PostRepository
from app.repositories.topic_repository import TopicRepository
from app.utils.text_similarity import calculate_similarity


@dataclass
class SimilarityCheckResult:
    is_similar: bool
    similarity_score: float
    matched_text: str | None = None


class MemoryEngine:
    """Manages agent memory in PostgreSQL and checks similarity against existing published posts/topics."""

    def __init__(
        self,
        session: AsyncSession,
        similarity_threshold: float = 0.65,
    ) -> None:
        self.session = session
        self.topic_repo = TopicRepository(session)
        self.post_repo = PostRepository(session)
        self.similarity_threshold = similarity_threshold

    async def check_similarity(
        self,
        title: str,
        summary: str,
        url: str,
    ) -> SimilarityCheckResult:
        """Check if topic URL, title, or summary closely matches previously PUBLISHED topics or posts."""
        # 1. Check exact URL match against PUBLISHED topics
        existing_topic = await self.topic_repo.get_by_url(url)
        if existing_topic and existing_topic.status == TopicStatus.PUBLISHED:
            return SimilarityCheckResult(
                is_similar=True,
                similarity_score=1.0,
                matched_text=existing_topic.title,
            )

        new_text = f"{title} {summary}"

        # 2. Check recent published posts
        posts = await self.post_repo.get_all_recent_posts(limit=100)
        for post in posts:
            score = calculate_similarity(new_text, post.text)
            if score >= self.similarity_threshold:
                return SimilarityCheckResult(
                    is_similar=True,
                    similarity_score=score,
                    matched_text=post.text[:100],
                )

        # 3. Check recently published topics
        recent_topics = await self.topic_repo.list_recent_topics(limit=100)
        for topic in recent_topics:
            if topic.status == TopicStatus.PUBLISHED:
                topic_text = f"{topic.title} {topic.summary}"
                score = calculate_similarity(new_text, topic_text)
                if score >= self.similarity_threshold:
                    return SimilarityCheckResult(
                        is_similar=True,
                        similarity_score=score,
                        matched_text=topic.title,
                    )

        return SimilarityCheckResult(
            is_similar=False,
            similarity_score=0.0,
            matched_text=None,
        )

    async def get_recent_posts_context(self, limit: int = 5) -> list[str]:
        """Fetch recent post texts to pass as context to LLM prompt builder."""
        posts = await self.post_repo.get_all_recent_posts(limit=limit)
        return [p.text for p in posts]
