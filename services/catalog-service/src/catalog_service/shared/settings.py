from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, read from environment variables and `.env`.

    Every variable is prefixed with `CATALOG_SERVICE_`, for example
    `CATALOG_SERVICE_PORT=8000`. `.env` is read from the current directory, so
    run the service from the repository root.
    """

    model_config = SettingsConfigDict(
        env_prefix="CATALOG_SERVICE_", env_file=".env", extra="ignore"
    )

    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings, loaded once."""
    return Settings()
