from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'
    )

    PROJECT_NAME = "HelenFlowers"
    API_VERSION_PREFIX = "/api/v1"
    ENVIRONMENT: Literal["production", "dev", "test"] = "dev"
    DEBUG: bool

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
            )
        )

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def REDIS_URL(self) -> str:
        return str(
            RedisDsn.build(
                scheme='redis',
                host=self.REDIS_HOST,
                port=self.REDIS_PORT,
                path="0",
            )
        )
    CELERY_BROKER_URL: str | None = None
    CELERY_RESULT_BACKEND: str | None = None

    SUPERUSER_EMAIL: str = "admin@helenflower.com"
    SUPERUSER_PASSWORD: str = "secret"

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    STORAGE_BACKEND: Literal["local", "s3"] = "local"
    MEDIA_ROOT = "/app/media/"
    MEDIA_URL_PREFIX: str = "/media"

    @property
    def celery_broker_url(self) -> str:
        return self.CELERY_BROKER_URL or self.REDIS_URL

    @property
    def celery_backend_url(self) -> str:
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()



