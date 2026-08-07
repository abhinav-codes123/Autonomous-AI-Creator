"""Tests for topic discovery providers."""

import pytest
from app.services.discovery.arxiv import ArxivProvider
from app.services.discovery.github_trending import GitHubTrendingProvider
from app.services.discovery.hacker_news import HackerNewsProvider
from app.services.discovery.rss_feed import RSSFeedProvider


@pytest.mark.asyncio
async def test_hacker_news_provider():
    provider = HackerNewsProvider(limit=3)
    topics = await provider.fetch_topics()
    assert isinstance(topics, list)
    if topics:
        first = topics[0]
        assert first.title
        assert first.url
        assert first.source_name == "Hacker News"


@pytest.mark.asyncio
async def test_github_trending_provider():
    provider = GitHubTrendingProvider()
    topics = await provider.fetch_topics()
    assert isinstance(topics, list)
    if topics:
        first = topics[0]
        assert first.title
        assert first.url
        assert first.source_name == "GitHub Trending"


@pytest.mark.asyncio
async def test_arxiv_provider():
    provider = ArxivProvider()
    topics = await provider.fetch_topics()
    assert isinstance(topics, list)
    if topics:
        first = topics[0]
        assert first.title
        assert first.url
        assert first.source_name == "arXiv"
