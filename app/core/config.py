"""Application Configuration settings."""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous AI Persona Backend"
    API_V1_STR: str = "/api"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./autonomous_agent.db"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql://") and not v.startswith("postgresql+"):
                return v.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif v.startswith("sqlite://") and not v.startswith("sqlite+"):
                return v.replace("sqlite://", "sqlite+aiosqlite://", 1)
        return v

    # LLM Settings
    OPENAI_API_KEY: str | None = None
    LLM_PROVIDER: str = "mock"  # openai, mock
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Scheduler (Default 1 minute for interactive testing & demo)
    SCHEDULER_INTERVAL_MINUTES: int = 1

    # Editorial & Memory Thresholds
    EDITORIAL_MIN_SCORE: float = 20.0
    MEMORY_SIMILARITY_THRESHOLD: float = 0.65
    
    RESET_DATABASE_ON_INIT: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
