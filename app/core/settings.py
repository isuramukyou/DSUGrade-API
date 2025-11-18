from functools import lru_cache
from typing import Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file='.env',
        env_file_encoding="utf-8",
    )


class UvicornSettings(EnvSettings, env_prefix="UVICORN_"):
    host: str
    port: int


class FastAPISettings(EnvSettings, env_prefix="FASTAPI_"):
    docs_url: Optional[str] = '/dsugrade-docs'
    openapi_url: Optional[str] = '/dsugrade-openapi.json'
    redoc_url: Optional[str] = '/dsugrade-redoc'
    cors_allow_origins: list[str] = ["*"]
    use_api_prefix: bool = False


class RedisSettings(EnvSettings, env_prefix="REDIS_"):
    host: str
    password: SecretStr
    port: int
    db: int

    def build_url(self) -> str:
        return f"redis://:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    uvicorn: UvicornSettings
    fastapi: FastAPISettings
    redis: RedisSettings


# noinspection PyArgumentList
settings = Settings(
    uvicorn=UvicornSettings(),
    fastapi=FastAPISettings(),
    redis=RedisSettings(),
)


@lru_cache()
def get_settings() -> Settings:
    return settings
