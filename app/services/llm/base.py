"""Base LLM Provider interface and response schema."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class LLMGeneratedContent:
    text: str
    rationale: str
    sources: list[str] = field(default_factory=list)


class LLMProvider(ABC):
    """Abstract base class for interchangeable LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str) -> LLMGeneratedContent:
        """Generate content from prompt asynchronously."""
        pass
