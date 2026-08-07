"""Tests for Editorial Engine scoring and rejection rules."""

from datetime import datetime, timezone
import pytest
from app.services.discovery.base import TopicData
from app.services.editorial.editorial_engine import EditorialEngine
from app.services.persona.persona_engine import PersonaEngine


@pytest.mark.asyncio
async def test_editorial_scoring_accepted():
    engine = EditorialEngine(min_score_threshold=20.0)
    persona_engine = PersonaEngine()
    persona = persona_engine.build_profile(name="Ada", domain="AI Security")

    topic = TopicData(
        title="New Prompt Injection Attack Vector in Large Language Models",
        summary="Researchers discover a zero-day prompt injection vulnerability bypassing alignment filters.",
        url="https://arxiv.org/abs/2401.99999",
        published_time=datetime.now(timezone.utc),
        source_name="arXiv",
    )

    score = engine.evaluate_topic(topic, persona)
    assert score.is_accepted is True
    assert score.final_score >= 20.0
    assert score.persona_fit >= 5.0
    assert score.rejection_reason is None


@pytest.mark.asyncio
async def test_editorial_rejection_clickbait():
    engine = EditorialEngine()
    persona_engine = PersonaEngine()
    persona = persona_engine.build_profile(name="Ada", domain="AI Security")

    topic = TopicData(
        title="You won't believe this shocking reason AI models fail!",
        summary="Clickbait summary about AI models.",
        url="https://example.com/clickbait",
        published_time=datetime.now(timezone.utc),
        source_name="Blog",
    )

    score = engine.evaluate_topic(topic, persona)
    assert score.is_accepted is False
    assert "Clickbait" in score.rejection_reason


@pytest.mark.asyncio
async def test_editorial_rejection_duplicate():
    engine = EditorialEngine()
    persona_engine = PersonaEngine()
    persona = persona_engine.build_profile(name="Ada", domain="AI Security")

    topic = TopicData(
        title="Model Jailbreaks via Adversarial Prompts",
        summary="Detailed study on model jailbreaks.",
        url="https://arxiv.org/abs/2401.88888",
        published_time=datetime.now(timezone.utc),
        source_name="arXiv",
    )

    score = engine.evaluate_topic(topic, persona, is_duplicate=True, similarity_score=0.9)
    assert score.is_accepted is False
    assert score.rejection_reason == "Already discussed"
