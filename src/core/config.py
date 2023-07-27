from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    app_title: str = 'downloader_manager'
    env_name: str = "'downloader_manager"
    base_url: str = "http://localhost:8000"
    database_dsn: PostgresDsn

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
