from pathlib import Path

import pytest

from import_worker.shared.settings import Settings, get_settings


def test_settings_read_prefixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMPORT_WORKER_POLL_INTERVAL_SECONDS", "1.5")

    assert Settings().poll_interval_seconds == 1.5


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.inbox_dir == Path("data/inbox")
    assert settings.catalog_url == "http://localhost:8000"


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
