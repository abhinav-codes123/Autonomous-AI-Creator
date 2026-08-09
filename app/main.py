"""Main FastAPI Application Entrypoint."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.db.base import Base
from app.db.session import engine
from app.scheduler.autonomous_scheduler import autonomous_scheduler


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

    # Start background scheduler
    autonomous_scheduler.start()
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
