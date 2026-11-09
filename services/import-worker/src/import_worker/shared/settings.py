from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings, read from environment variables and `.env`.

    Every variable is prefixed with `IMPORT_WORKER_`, for example
    `IMPORT_WORKER_POLL_INTERVAL_SECONDS=5`. Relative paths and `.env` are
    resolved from the current directory, so run the worker from the
    repository root.
    """

    model_config = SettingsConfigDict(
        env_prefix="IMPORT_WORKER_", env_file=".env", extra="ignore"
    )

    inbox_dir: Path = Path("data/inbox")
    processed_dir: Path = Path("data/processed")
    failed_dir: Path = Path("data/failed")
    poll_interval_seconds: float = 5.0
    catalog_url: str = "http://localhost:8000"
    catalog_timeout_seconds: float = 5.0
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings, loaded once."""
    return Settings()
