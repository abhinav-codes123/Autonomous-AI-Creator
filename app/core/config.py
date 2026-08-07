"""Application Configuration settings."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous AI Persona Backend"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./autonomous_agent.db"
    )

    # LLM Settings
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai, mock
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Scheduler
    SCHEDULER_INTERVAL_MINUTES: int = int(os.getenv("SCHEDULER_INTERVAL_MINUTES", "30"))

    # Editorial & Memory Thresholds
    EDITORIAL_MIN_SCORE: float = float(os.getenv("EDITORIAL_MIN_SCORE", "20.0"))
    MEMORY_SIMILARITY_THRESHOLD: float = float(os.getenv("MEMORY_SIMILARITY_THRESHOLD", "0.65"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
