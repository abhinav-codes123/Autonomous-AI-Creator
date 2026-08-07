"""arXiv Topic Provider."""

from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import httpx
from app.core.logging import logger
from app.services.discovery.base import TopicData, TopicProvider


class ArxivProvider(TopicProvider):
    ARXIV_API_URL = (
        "http://export.arxiv.org/api/query?"
        "search_query=cat:cs.AI+OR+cat:cs.CR+OR+cat:cs.CL&"
        "sortBy=submittedDate&sortOrder=descending&max_results=10"
    )

    async def fetch_topics(self) -> list[TopicData]:
        topics: list[TopicData] = []
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(self.ARXIV_API_URL)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.text)
                    ns = {"atom": "http://www.w3.org/2005/Atom"}
                    for entry in root.findall("atom:entry", ns):
                        title_elem = entry.find("atom:title", ns)
                        summary_elem = entry.find("atom:summary", ns)
                        id_elem = entry.find("atom:id", ns)
                        published_elem = entry.find("atom:published", ns)

                        if title_elem is not None and id_elem is not None:
                            title = " ".join(title_elem.text.split())
                            summary = " ".join(summary_elem.text.split()) if summary_elem is not None else ""
                            url = id_elem.text.strip()
                            pub_str = published_elem.text.strip() if published_elem is not None else ""
                            try:
                                pub_time = datetime.fromisoformat(pub_str.replace("Z", "+00:00"))
                            except Exception:
                                pub_time = datetime.now(timezone.utc)

                            topics.append(
                                TopicData(
                                    title=f"[Paper] {title}",
                                    summary=summary[:600],
                                    url=url,
                                    published_time=pub_time,
                                    source_name="arXiv",
                                )
                            )
        except Exception as e:
            logger.error(f"Error fetching from arXiv: {e}")

        return topics
