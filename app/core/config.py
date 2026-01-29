from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Telegram Commerce"
    DATABASE_URL: str
    JWT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()