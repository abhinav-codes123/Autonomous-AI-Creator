"""Autonomous Scheduler service using APScheduler for background post generation."""

import asyncio
import time
from datetime import datetime, timezone
import uuid
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.core.logging import logger
from app.db.session import AsyncSessionLocal
from app.services.publishing.publishing_service import PublishingService


class AutonomousScheduler:
    """Manages background scheduled execution for autonomous content generation with concurrency safety."""

    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        self._lock = asyncio.Lock()
        self._last_run_timestamp = 0.0
        self.cycle_count = 0
        self.cycle_history: list[dict] = []

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

    async def _scheduled_job(self) -> None:
        """Periodic background job callback with lock protection."""
        if self._lock.locked():
            logger.info("Autonomous cycle already in progress, skipping periodic run.")
            return

        # Cooldown guard (at least 10s between cycles)
        now_ts = time.time()
        if self._last_run_timestamp > 0 and (now_ts - self._last_run_timestamp) < 10.0:
            logger.info("Autonomous cycle ran recently, skipping redundant execution.")
            return

        async with self._lock:
            start_ts = time.time()
            start_iso = datetime.now(timezone.utc).isoformat()
            self.cycle_count += 1
            cycle_num = self.cycle_count
            interval_from_last = start_ts - self._last_run_timestamp if self._last_run_timestamp > 0 else 0.0

            logger.info(f"[SCHEDULER] Starting cycle #{cycle_num} for active agents at {start_iso}")
            
            posts_created = 0
            async with AsyncSessionLocal() as session:
                service = PublishingService(session)
                posts = await service.run_autonomous_cycle()
                posts_created = len(posts)
                self._last_run_timestamp = time.time()

            end_ts = time.time()
            end_iso = datetime.now(timezone.utc).isoformat()
            duration = end_ts - start_ts

            metrics = {
                "cycle": cycle_num,
                "start": start_iso,
                "end": end_iso,
                "duration_seconds": round(duration, 3),
                "interval_seconds": round(interval_from_last, 3),
                "posts_created": posts_created,
            }
            self.cycle_history.append(metrics)
            logger.info(
                f"[SCHEDULER] Cycle #{cycle_num} finished in {duration:.2f}s "
                f"(Interval: {interval_from_last:.1f}s, Posts: {posts_created})"
            )


autonomous_scheduler = AutonomousScheduler()
