from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from catalog_service.api.app import create_app
from catalog_service.api.dependencies import get_item_repository
from fakes import FakeItemRepository


@pytest.fixture
def fake_repository() -> FakeItemRepository:
    return FakeItemRepository()


@pytest.fixture
def client(fake_repository: FakeItemRepository) -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_item_repository] = lambda: fake_repository
    with TestClient(app) as test_client:
        yield test_client
