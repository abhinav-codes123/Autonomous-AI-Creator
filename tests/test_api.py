"""API integration tests for init and feed endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.post_repository import PostRepository
from app.repositories.agent_repository import AgentRepository


@pytest.mark.asyncio
async def test_init_agent_endpoint(async_client: AsyncClient):
    payload = {
        "persona": {
            "name": "Ada",
            "domain": "AI Security"
        }
    }
    response = await async_client.post("/api/agent/init", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "agentId" in data
    assert len(data["agentId"]) > 0


@pytest.mark.asyncio
async def test_get_agent_feed_endpoint(async_client: AsyncClient, db_session: AsyncSession):
    # 1. Create agent
    agent_repo = AgentRepository(db_session)
    agent = await agent_repo.create(name="Ada", domain="AI Security")

    # 2. Add sample posts to DB
    post_repo = PostRepository(db_session)
    await post_repo.create_post(
        agent_id=agent.id,
        text="First post commentary on AI security.",
        rationale="Selected due to high relevance.",
        sources=["https://arxiv.org/abs/2401.00001"],
    )
    await post_repo.create_post(
        agent_id=agent.id,
        text="Second newer post commentary on prompt injection.",
        rationale="Selected due to novel attack vector.",
        sources=["https://hacker-news.com/item?id=123"],
    )

    # 3. Query feed
    response = await async_client.get(f"/api/agent/feed?agentId={agent.id}")
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert len(data["posts"]) == 2

    # Check newest first order
    posts = data["posts"]
    assert "Second newer post" in posts[0]["text"]
    assert "First post" in posts[1]["text"]
    assert posts[0]["sources"] == ["https://hacker-news.com/item?id=123"]


@pytest.mark.asyncio
async def test_get_agent_feed_not_found(async_client: AsyncClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.get(f"/api/agent/feed?agentId={fake_id}")
    assert response.status_code == 404
