"""GitHub Trending / Search Topic Provider."""

from datetime import datetime, timezone
import httpx
from bs4 import BeautifulSoup
from app.core.logging import logger
from app.services.discovery.base import TopicData, TopicProvider


class GitHubTrendingProvider(TopicProvider):
    GITHUB_SEARCH_URL = "https://api.github.com/search/repositories?q=AI+security+OR+LLM+security&sort=stars&order=desc"
    GITHUB_TRENDING_URL = "https://github.com/trending/python?since=daily"

    async def fetch_topics(self) -> list[TopicData]:
        topics: list[TopicData] = []
        headers = {"User-Agent": "Mozilla/5.0 (Autonomous-AI-Creator)"}

        # Method 1: Try GitHub Search API
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
                resp = await client.get(self.GITHUB_SEARCH_URL)
                if resp.status_code == 200:
                    items = resp.json().get("items", [])[:10]
                    for item in items:
                        url = item["html_url"]
                        title = f"{item['full_name']}: {item.get('description', '')}"
                        summary = f"GitHub repository {item['full_name']} with {item['stargazers_count']} stars. Language: {item.get('language', 'Python')}."
                        topics.append(
                            TopicData(
                                title=title[:255],
                                summary=summary,
                                url=url,
                                published_time=datetime.now(timezone.utc),
                                source_name="GitHub Trending",
                            )
                        )
                    if topics:
                        return topics
        except Exception as e:
            logger.warning(f"Error fetching GitHub Search API: {e}")

        # Method 2: Fallback HTML scrape of GitHub Trending
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=headers, follow_redirects=True) as client:
                resp = await client.get(self.GITHUB_TRENDING_URL)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    articles = soup.find_all("article", class_="Box-row")[:10]
                    for article in articles:
                        h2 = article.find("h2")
                        if h2 and h2.find("a"):
                            repo_path = h2.find("a")["href"].strip()
                            url = f"https://github.com{repo_path}"
                            repo_name = repo_path.strip("/")
                            p = article.find("p")
                            desc = p.text.strip() if p else "No description"
                            topics.append(
                                TopicData(
                                    title=f"GitHub Trending: {repo_name}",
                                    summary=desc,
                                    url=url,
                                    published_time=datetime.now(timezone.utc),
                                    source_name="GitHub Trending",
                                )
                            )
        except Exception as e:
            logger.error(f"Error scraping GitHub Trending: {e}")

        return topics
