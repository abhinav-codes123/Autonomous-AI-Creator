"""Application Configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous AI Persona Backend"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./autonomous_agent.db"

    # LLM Settings
    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: str = "mock"  # openai, mock
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Scheduler (Default 1 minute for interactive testing & demo)
    SCHEDULER_INTERVAL_MINUTES: int = 1

    # Editorial & Memory Thresholds
    EDITORIAL_MIN_SCORE: float = 20.0
    MEMORY_SIMILARITY_THRESHOLD: float = 0.65

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
