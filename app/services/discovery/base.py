"""Base generic interface for topic discovery providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class TopicData:
    title: str
    summary: str
    url: str
    published_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    source_name: str = "Unknown"


class TopicProvider(ABC):
    """Abstract base class for all topic providers."""

    @abstractmethod
    async def fetch_topics(self) -> list[TopicData]:
        """Fetch topics asynchronously from the source."""
        pass
