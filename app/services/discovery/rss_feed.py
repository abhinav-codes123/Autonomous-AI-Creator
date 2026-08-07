"""RSS Feed Topic Provider for AI Industry blogs (OpenAI, Anthropic, DeepMind, TechCrunch)."""

from datetime import datetime, timezone
import feedparser
import httpx
from app.core.logging import logger
from app.services.discovery.base import TopicData, TopicProvider


class RSSFeedProvider(TopicProvider):
    DEFAULT_FEEDS = [
        ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
        ("OpenAI Blog", "https://openai.com/news/rss.xml"),
        ("Anthropic Research", "https://www.anthropic.com/feed.xml"),
        ("Google DeepMind", "https://deepmind.google/blog/rss.xml"),
        ("MIT Tech Review AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ]

    def __init__(self, feeds: list[tuple[str, str]] | None = None) -> None:
        self.feeds = feeds or self.DEFAULT_FEEDS

    async def fetch_topics(self) -> list[TopicData]:
        topics: list[TopicData] = []
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            for name, feed_url in self.feeds:
                try:
                    resp = await client.get(feed_url, headers={"User-Agent": "Mozilla/5.0 (Autonomous-AI-Creator)"})
                    if resp.status_code == 200:
                        parsed = feedparser.parse(resp.text)
                        for entry in parsed.entries[:5]:
                            title = getattr(entry, "title", "No Title")
                            url = getattr(entry, "link", "")
                            summary = getattr(entry, "summary", getattr(entry, "description", ""))

                            if not url:
                                continue

                            topics.append(
                                TopicData(
                                    title=title,
                                    summary=summary[:600] if summary else title,
                                    url=url,
                                    published_time=datetime.now(timezone.utc),
                                    source_name=name,
                                )
                            )
                except Exception as e:
                    logger.warning(f"Failed to fetch RSS feed {name} ({feed_url}): {e}")

        return topics
