from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, read from environment variables and `.env`.

    Every variable is prefixed with `ORDER_SERVICE_`, for example
    `ORDER_SERVICE_PORT=8001`. `.env` is read from the current directory, so
    run the service from the repository root.
    """

    model_config = SettingsConfigDict(
        env_prefix="ORDER_SERVICE_", env_file=".env", extra="ignore"
    )

    host: str = "0.0.0.0"
    port: int = 8001
    log_level: str = "info"
    catalog_url: str = "http://localhost:8000"
    catalog_timeout_seconds: float = 5.0


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings, loaded once."""
    return Settings()
