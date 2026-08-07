"""End-to-end tests for Publishing Service and Autonomous Cycle."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.topic import TopicStatus
from app.repositories.agent_repository import AgentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.topic_repository import TopicRepository
from app.services.publishing.publishing_service import PublishingService


@pytest.mark.asyncio
async def test_publishing_service_end_to_end(db_session: AsyncSession):
    # 1. Create Agent
    agent_repo = AgentRepository(db_session)
    agent = await agent_repo.create(name="Ada", domain="AI Security")

    # 2. Instantiate Publishing Service
    service = PublishingService(session=db_session)

    # 3. Run autonomous cycle
    posts = await service.run_autonomous_cycle(agent_id=agent.id)

    assert len(posts) > 0
    first_post = posts[0]
    assert first_post.agent_id == agent.id
    assert len(first_post.text) > 50
    assert "Selection Rationale:" in first_post.rationale or len(first_post.rationale) > 20
    assert len(first_post.sources) > 0

    # 4. Verify Post is retrievable via PostRepository
    post_repo = PostRepository(db_session)
    retrieved_posts = await post_repo.get_posts_by_agent(agent.id)
    assert len(retrieved_posts) == len(posts)
    assert str(retrieved_posts[0].id) == str(first_post.id)
