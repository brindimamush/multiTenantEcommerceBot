from pydantic_settings import BaseSettings
from pydantic import Field

"""
Settings are loaded in multiple contexts:
- Runtime (FASTAPI)
- Migration (Alembic)

Not all fields are needed in both contexts."""

class Settings(BaseSettings):
    APP_NAME: str = "Telegram Commerce"
    # Async URL (used by FastAPI)
    DATABASE_URL:str
    # Sync URL (used by Alembic)
    DATABASE_URL_SYNC: str | None = None
    # JWT Secret for signing tokens
    JWT_SECRET: str | None = Field(default=None)

    class Config:
        env_file = ".env"

settings = Settings()

# Derive sync URL automatically
if settings.DATABASE_URL.startswith("postgresql+asyncpg"):
    settings.DATABASE_URL_SYNC = settings.DATABASE_URL.replace(
        "postgresql+asyncpg", "postgresql+psycopg2",
    )