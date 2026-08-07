"""LLM service package export and factory."""

from app.core.config import settings
from app.services.llm.base import LLMGeneratedContent, LLMProvider
from app.services.llm.mock_provider import MockLLMProvider
from app.services.llm.openai_provider import OpenAIProvider


def get_llm_provider() -> LLMProvider:
    """Factory function returning the configured LLM provider."""
    if settings.LLM_PROVIDER.lower() == "openai" and settings.OPENAI_API_KEY:
        return OpenAIProvider(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
        )
    return MockLLMProvider()


__all__ = [
    "LLMGeneratedContent",
    "LLMProvider",
    "OpenAIProvider",
    "MockLLMProvider",
    "get_llm_provider",
]
