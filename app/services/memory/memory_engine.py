"""Memory Engine for checking historical posts, covered topics, and deduplication."""

from dataclasses import dataclass
import uuid
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
        agent_id: uuid.UUID | None = None,
    ) -> SimilarityCheckResult:
        """Check if topic URL, title, or summary closely matches previously PUBLISHED topics or posts."""
        # Production callers must supply an agent ID. The optional value only
        # preserves compatibility with the original standalone utility API.
        if agent_id is None:
            return await self._check_legacy_similarity(title, summary, url)

        # 1. Check exact URL match against this agent's PUBLISHED topics
        existing_topic = await self.topic_repo.get_by_url(url, agent_id)
        if existing_topic and existing_topic.status == TopicStatus.PUBLISHED:
            return SimilarityCheckResult(
                is_similar=True,
                similarity_score=1.0,
                matched_text=existing_topic.title,
            )

        new_text = f"{title} {summary}"

        # 2. Check recently published topics.  Topic titles and summaries are
        # stable memory signals; generated post prose contains persona boilerplate
        # and would incorrectly suppress unrelated stories in the same domain.
        recent_topics = await self.topic_repo.list_recent_topics(limit=100, agent_id=agent_id)
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

    async def _check_legacy_similarity(
        self, title: str, summary: str, url: str
    ) -> SimilarityCheckResult:
        """Compatibility helper for direct utility callers without an agent.

        Scheduled publishing never uses this path; all of its memory reads are
        scoped to the publishing agent.
        """
        new_text = f"{title} {summary}"
        for post in await self.post_repo.get_all_recent_posts(limit=100):
            score = calculate_similarity(new_text, post.text)
            if score >= self.similarity_threshold:
                return SimilarityCheckResult(True, score, post.text[:100])
        return SimilarityCheckResult(False, 0.0)

    async def get_recent_posts_context(self, agent_id: uuid.UUID, limit: int = 5) -> list[str]:
        """Fetch recent post texts to pass as context to LLM prompt builder."""
        posts = await self.post_repo.get_recent_posts_by_agent(agent_id, limit=limit)
        return [p.text for p in posts]
