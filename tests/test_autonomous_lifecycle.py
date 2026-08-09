"""Deterministic verification of autonomous-cycle persistence semantics."""

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import TopicStatus
from app.repositories.agent_repository import AgentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.topic_repository import TopicRepository
from app.services.discovery.base import TopicData, TopicProvider
from app.services.publishing.publishing_service import PublishingService


class StaticLiveTopics(TopicProvider):
    """A stable stand-in for live discovery used only by this test."""

    async def fetch_topics(self) -> list[TopicData]:
        return [
            TopicData(
                title="AI Security: New Prompt Injection Attack Vector in Large Language Models",
                summary="Researchers describe a prompt injection weakness that bypasses tool-use controls.",
                url="https://example.com/live/prompt-injection",
                published_time=datetime.now(timezone.utc),
                source_name="Test live source",
            ),
            TopicData(
                title="AI Security Vulnerability in AI Agent Tool Permissions",
                summary="Researchers identify an authorization flaw that can expose privileged agent actions.",
                url="https://example.com/live/supply-chain",
                published_time=datetime.now(timezone.utc),
                source_name="Test live source",
            ),
        ]


@pytest.mark.asyncio
async def test_cycles_publish_once_and_keep_agent_scoped_memory(db_session: AsyncSession):
    agent = await AgentRepository(db_session).create("Ada", "AI Security")
    service = PublishingService(db_session, providers=[StaticLiveTopics()])

    first_cycle = await service.run_autonomous_cycle(agent.id)
    second_cycle = await service.run_autonomous_cycle(agent.id)
    third_cycle = await service.run_autonomous_cycle(agent.id)

    assert len(first_cycle) == 1
    assert len(second_cycle) == 1
    assert third_cycle == []

    posts = await PostRepository(db_session).get_posts_by_agent(agent.id)
    assert len(posts) == 2
    assert all(post.agent_id == agent.id for post in posts)
    assert all(source.url.startswith("https://") for post in posts for source in post.sources)

    topics = await TopicRepository(db_session).list_recent_topics(agent_id=agent.id)
    assert len(topics) == 2
    assert all(topic.status == TopicStatus.PUBLISHED for topic in topics)
