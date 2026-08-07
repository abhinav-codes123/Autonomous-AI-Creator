"""Tests for Memory Engine text similarity and deduplication."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.post_repository import PostRepository
from app.repositories.agent_repository import AgentRepository
from app.services.memory.memory_engine import MemoryEngine
from app.utils.text_similarity import calculate_similarity, jaccard_similarity


def test_text_similarity_utils():
    text1 = "Prompt Injection Vulnerability in LLMs"
    text2 = "Prompt Injection Vulnerability in Large Language Models"
    text3 = "Quantum computing error correction using superconducting qubits"

    sim12 = calculate_similarity(text1, text2)
    jaccard13 = jaccard_similarity(text1, text3)

    assert sim12 > 0.5
    assert jaccard13 == 0.0


@pytest.mark.asyncio
async def test_memory_engine_similarity_check(db_session: AsyncSession):
    agent_repo = AgentRepository(db_session)
    agent = await agent_repo.create("Ada", "AI Security")

    post_repo = PostRepository(db_session)
    await post_repo.create_post(
        agent_id=agent.id,
        text="Analysis of Zero-day Prompt Injection Attacks in LLMs",
        rationale="High importance topic",
        sources=["https://example.com/source1"],
    )

    memory_engine = MemoryEngine(db_session, similarity_threshold=0.6)

    # Check highly similar topic
    result = await memory_engine.check_similarity(
        title="Zero-day Prompt Injection Attacks in LLMs",
        summary="Analysis of zero-day prompt injection vulnerabilities.",
        url="https://example.com/different_url",
    )
    assert result.is_similar is True

    # Check completely different topic
    result_different = await memory_engine.check_similarity(
        title="Unrelated Distributed Systems Benchmark",
        summary="Benchmarking Redis vs Memcached performance.",
        url="https://example.com/distributed",
    )
    assert result_different.is_similar is False
