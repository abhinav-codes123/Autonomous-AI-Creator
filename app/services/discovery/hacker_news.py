"""Hacker News Topic Provider."""

from datetime import datetime, timezone
import httpx
from app.core.logging import logger
from app.services.discovery.base import TopicData, TopicProvider


class HackerNewsProvider(TopicProvider):
    TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    def __init__(self, limit: int = 15) -> None:
        self.limit = limit

    async def fetch_topics(self) -> list[TopicData]:
        topics: list[TopicData] = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(self.TOP_STORIES_URL)
                if resp.status_code != 200:
                    logger.warning(f"HackerNews API returned status {resp.status_code}")
                    return topics

                story_ids = resp.json()[:self.limit]
                for story_id in story_ids:
                    item_resp = await client.get(self.ITEM_URL.format(story_id))
                    if item_resp.status_code == 200:
                        data = item_resp.json()
                        if data and data.get("type") == "story" and "title" in data:
                            url = data.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
                            title = data["title"]
                            text = data.get("text", "") or f"Hacker News story by {data.get('by', 'user')} with {data.get('score', 0)} points."
                            time_unix = data.get("time", 0)
                            pub_time = datetime.fromtimestamp(time_unix, tz=timezone.utc) if time_unix else datetime.now(timezone.utc)

                            topics.append(
                                TopicData(
                                    title=title,
                                    summary=text[:500],
                                    url=url,
                                    published_time=pub_time,
                                    source_name="Hacker News",
                                )
                            )
        except Exception as e:
            logger.error(f"Error fetching from Hacker News: {e}")

        return topics
