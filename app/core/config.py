from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MediVue Task Management API"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./task_manager.db"
    default_limit: int = 20
    max_limit: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
