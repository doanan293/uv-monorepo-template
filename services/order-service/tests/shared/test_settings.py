import pytest

from order_service.shared.settings import Settings, get_settings


def test_settings_read_prefixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ORDER_SERVICE_CATALOG_URL", "http://catalog:9000")

    assert Settings().catalog_url == "http://catalog:9000"


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.port == 8001
    assert settings.catalog_url == "http://localhost:8000"


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
