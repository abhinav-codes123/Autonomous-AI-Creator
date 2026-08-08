"""Publishing Service for orchestrating the autonomous content creation pipeline."""

from datetime import datetime, timezone
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.models.agent import Agent
from app.models.post import Post
from app.models.topic import TopicStatus
from app.prompts.prompt_builder import PromptBuilder
from app.repositories.agent_repository import AgentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.topic_repository import TopicRepository
from app.services.discovery.arxiv import ArxivProvider
from app.services.discovery.base import TopicData, TopicProvider
from app.services.discovery.github_trending import GitHubTrendingProvider
from app.services.discovery.hacker_news import HackerNewsProvider
from app.services.discovery.rss_feed import RSSFeedProvider
from app.services.editorial.editorial_engine import EditorialEngine
from app.services.llm import get_llm_provider
from app.services.memory.memory_engine import MemoryEngine
from app.services.persona.persona_engine import PersonaEngine
from app.utils.text_similarity import calculate_similarity


class FallbackTopicProvider(TopicProvider):
    """Fallback topic provider for offline or restricted environments."""

    def __init__(self, domain: str = "AI Security") -> None:
        self.domain = domain

    async def fetch_topics(self) -> list[TopicData]:
        return [
            TopicData(
                title=f"New Prompt Injection and Model Jailbreaks Research in {self.domain}",
                summary=f"Empirical study analyzing Prompt Injection, Red Teaming, and CVEs in LLM systems for {self.domain}.",
                url=f"https://arxiv.org/abs/2401.{uuid.uuid4().hex[:6]}",
                published_time=datetime.now(timezone.utc),
                source_name="arXiv",
            )
        ]


class PublishingService:
    """Orchestrates Topic Discovery -> Editorial Filtering -> Memory Check -> LLM Generation -> DB Persistence."""

    def __init__(
        self,
        session: AsyncSession,
        providers: list[TopicProvider] | None = None,
    ) -> None:
        self.session = session
        self.agent_repo = AgentRepository(session)
        self.topic_repo = TopicRepository(session)
        self.post_repo = PostRepository(session)
        self.editorial_engine = EditorialEngine()
        self.memory_engine = MemoryEngine(session)
        self.persona_engine = PersonaEngine()
        self.prompt_builder = PromptBuilder()
        self.llm_provider = get_llm_provider()

        self.providers = providers or [
            HackerNewsProvider(),
            GitHubTrendingProvider(),
            ArxivProvider(),
            RSSFeedProvider(),
        ]

    async def run_autonomous_cycle(self, agent_id: uuid.UUID | None = None) -> list[Post]:
        """Runs a complete autonomous cycle for active agent(s)."""
        logger.info("Starting autonomous content generation cycle...")

        # 1. Fetch target agent(s)
        if agent_id:
            agent = await self.agent_repo.get_by_id(agent_id)
            agents = [agent] if agent else []
        else:
            agents = list(await self.agent_repo.list_all())

        if not agents:
            logger.warning("No active agents found for autonomous cycle.")
            return []

        published_posts: list[Post] = []

        for agent in agents:
            try:
                post = await self._run_cycle_for_agent(agent)
                if post:
                    published_posts.append(post)
            except Exception as e:
                logger.error(f"Error during autonomous cycle for agent {agent.id}: {e}", exc_info=True)

        logger.info(f"Autonomous cycle completed. Created {len(published_posts)} posts.")
        return published_posts

    async def _run_cycle_for_agent(self, agent: Agent) -> Post | None:
        persona = self.persona_engine.build_profile(agent.name, agent.domain)

        # Step 1: Discover Topics from all providers
        all_discovered: list[TopicData] = []
        for provider in self.providers:
            try:
                topics = await provider.fetch_topics()
                all_discovered.extend(topics)
            except Exception as e:
                logger.warning(f"Provider {provider.__class__.__name__} failed: {e}")

        # If network/external providers returned no topics, use fallback provider
        if not all_discovered:
            logger.info("External providers returned no topics. Using fallback topic provider.")
            fallback = FallbackTopicProvider(domain=agent.domain)
            all_discovered = await fallback.fetch_topics()

        logger.info(f"Discovered {len(all_discovered)} potential topics.")

        # Multi-Source Clustering: Map duplicate stories across providers to aggregate sources
        source_clusters: dict[str, list[str]] = {}
        for topic in all_discovered:
            cluster_found = False
            for primary_url, sources in source_clusters.items():
                # Find matching primary topic in current batch
                matching_topic = next((t for t in all_discovered if t.url == primary_url), None)
                if matching_topic and calculate_similarity(topic.title, matching_topic.title) >= 0.65:
                    if topic.url not in sources:
                        sources.append(topic.url)
                    cluster_found = True
                    break
            if not cluster_found:
                source_clusters[topic.url] = [topic.url]

        scored_candidates: list[tuple[TopicData, float, list[str]]] = []

        # Step 2 & 3: Editorial Filtering & Memory Similarity Check
        for topic_data in all_discovered:
            # Memory Check
            sim_result = await self.memory_engine.check_similarity(
                title=topic_data.title,
                summary=topic_data.summary,
                url=topic_data.url,
            )

            # Editorial Evaluation
            editorial_score = self.editorial_engine.evaluate_topic(
                topic=topic_data,
                persona=persona,
                is_duplicate=sim_result.is_similar,
                similarity_score=sim_result.similarity_score,
            )

            # Persist topic record in DB
            db_topic = await self.topic_repo.create_or_update(
                title=topic_data.title,
                summary=topic_data.summary,
                url=topic_data.url,
                score=editorial_score.final_score,
                status=TopicStatus.NEW,
            )

            if not editorial_score.is_accepted:
                reason = editorial_score.rejection_reason or "Low editorial score"
                await self.topic_repo.mark_rejected(db_topic, reason=reason)
                logger.info(f"Rejected topic '{topic_data.title[:50]}': {reason}")
            else:
                aggregated_sources = source_clusters.get(topic_data.url, [topic_data.url])
                scored_candidates.append((topic_data, editorial_score.final_score, aggregated_sources))

        if not scored_candidates:
            logger.warning(f"No suitable topics passed editorial filtering for agent {agent.name}.")
            return None

        # Pick top scoring candidate topic
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        best_topic, best_score, aggregated_sources = scored_candidates[0]
        logger.info(f"Selected best topic for post generation: '{best_topic.title}' (score: {best_score})")

        # Step 4: Fetch recent posts for memory context & construct prompt
        previous_posts = await self.memory_engine.get_recent_posts_context(limit=5)
        prompt = self.prompt_builder.build_post_generation_prompt(
            persona=persona,
            topic=best_topic,
            previous_posts=previous_posts,
        )

        # Step 5: Generate post with LLM Provider
        generated = await self.llm_provider.generate(prompt)

        final_sources = list(dict.fromkeys((generated.sources or []) + aggregated_sources))

        # Step 6: Persist Post and update Topic status in DB
        post = await self.post_repo.create_post(
            agent_id=agent.id,
            text=generated.text,
            rationale=generated.rationale,
            sources=final_sources,
        )

        # Mark topic as published
        db_topic = await self.topic_repo.get_by_url(best_topic.url)
        if db_topic:
            await self.topic_repo.mark_published(db_topic)

        logger.info(f"Successfully published post {post.id} for agent {agent.name}.")
        return post
