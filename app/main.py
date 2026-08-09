"""Main FastAPI Application Entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.db.base import Base
from app.db.session import AsyncSessionLocal, engine
from app.repositories.agent_repository import AgentRepository
from app.scheduler.autonomous_scheduler import autonomous_scheduler


def _validate_database_schema(connection) -> None:
    """Fail loudly instead of running with a partially compatible SQLite schema."""
    inspector = inspect(connection)
    required = {
        "agents": {"id", "name", "domain", "is_active", "created_at"},
        "topics": {"id", "agent_id", "title", "summary", "url", "status", "discovered_at"},
        "posts": {"id", "agent_id", "text", "rationale", "created_at"},
        "post_sources": {"id", "post_id", "url"},
    }
    missing = {
        table: columns - {column["name"] for column in inspector.get_columns(table)}
        for table, columns in required.items()
        if inspector.has_table(table)
    }
    missing = {table: columns for table, columns in missing.items() if columns}
    if missing:
        details = "; ".join(f"{table}: {', '.join(sorted(columns))}" for table, columns in missing.items())
        raise RuntimeError(
            f"Outdated database schema ({details}). Run `alembic upgrade head` or "
            "the development reset script before starting the server."
        )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown procedures."""
    setup_logging()
    logger.info("Initializing Autonomous AI Persona Backend...")

    # Create database tables if they do not exist
    async with engine.begin() as conn:
        if settings.RESET_DATABASE_ON_INIT:
            logger.warning("DEVELOPMENT ONLY: Database reset on init.")
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_validate_database_schema)

    # Resume the scheduler only when active persisted agents exist.
    async with AsyncSessionLocal() as session:
        active_agents = await AgentRepository(session).list_active()
        if active_agents:
            autonomous_scheduler.start()
            logger.info(f"Resuming scheduler for {len(active_agents)} active agent(s).")
        else:
            logger.info("No active agent found on startup; scheduler remaining idle.")
    logger.info("Application startup complete.")

    yield

    # Shutdown procedure
    logger.info("Shutting down Application...")
    autonomous_scheduler.shutdown()
    await engine.dispose()
    logger.info("Application shutdown complete.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "project": settings.PROJECT_NAME}
