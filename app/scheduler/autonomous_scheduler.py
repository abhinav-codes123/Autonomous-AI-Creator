"""Autonomous Scheduler service using APScheduler for background post generation."""

import uuid
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.core.logging import logger
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.services.publishing.publishing_service import PublishingService


class AutonomousScheduler:
    """Manages background scheduled execution for autonomous content generation."""

    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    def start(self) -> None:
        if not self.is_running:
            self.scheduler.add_job(
                self._scheduled_job,
                "interval",
                minutes=settings.SCHEDULER_INTERVAL_MINUTES,
                id="autonomous_cycle_job",
                replace_existing=True,
            )
            self.scheduler.start()
            self.is_running = True
            logger.info(
                f"Autonomous Scheduler started. Running every {settings.SCHEDULER_INTERVAL_MINUTES} minutes."
            )

    def shutdown(self) -> None:
        if self.is_running:
            self.scheduler.shutdown(wait=False)
            self.is_running = False
            logger.info("Autonomous Scheduler shut down.")

    async def trigger_immediate_run(self, agent_id: uuid.UUID | None = None) -> None:
        """Trigger an immediate background run for a given agent or all agents."""
        logger.info(f"Triggering immediate autonomous run for agent_id: {agent_id}")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSessionLocal() as session:
            service = PublishingService(session)
            await service.run_autonomous_cycle(agent_id=agent_id)

    async def _scheduled_job(self) -> None:
        """Periodic background job callback."""
        logger.info("Scheduler executing periodic autonomous content cycle...")
        async with AsyncSessionLocal() as session:
            service = PublishingService(session)
            await service.run_autonomous_cycle()


autonomous_scheduler = AutonomousScheduler()
