from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str = ""
    USE_SQLITE: bool = False

    def get_db_url(self):
        if self.USE_SQLITE:
            return "sqlite+aiosqlite:///./sqlite_dev.db"
        return self.DATABASE_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()
