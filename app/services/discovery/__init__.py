"""Discovery service package export."""

from app.services.discovery.base import TopicData, TopicProvider
from app.services.discovery.hacker_news import HackerNewsProvider
from app.services.discovery.github_trending import GitHubTrendingProvider
from app.services.discovery.arxiv import ArxivProvider
from app.services.discovery.rss_feed import RSSFeedProvider

__all__ = [
    "TopicData",
    "TopicProvider",
    "HackerNewsProvider",
    "GitHubTrendingProvider",
    "ArxivProvider",
    "RSSFeedProvider",
]
