import pytest

from catalog_service.shared.settings import Settings, get_settings


def test_settings_read_prefixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CATALOG_SERVICE_PORT", "9000")

    assert Settings().port == 9000


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
