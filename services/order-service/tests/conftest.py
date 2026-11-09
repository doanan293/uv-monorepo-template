from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from fakes import FakeItemCatalog, FakeOrderRepository
from order_service.api.app import create_app
from order_service.api.dependencies import get_item_catalog, get_order_repository


@pytest.fixture
def fake_orders() -> FakeOrderRepository:
    return FakeOrderRepository()


@pytest.fixture
def fake_catalog() -> FakeItemCatalog:
    return FakeItemCatalog()


@pytest.fixture
def client(
    fake_orders: FakeOrderRepository, fake_catalog: FakeItemCatalog
) -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_order_repository] = lambda: fake_orders
    app.dependency_overrides[get_item_catalog] = lambda: fake_catalog
    with TestClient(app) as test_client:
        yield test_client
