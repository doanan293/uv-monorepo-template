from uuid import uuid4

import pytest

from fakes import FakeItemCatalog, FakeOrderRepository
from order_service.application.orders.place_order import PlaceOrder
from order_service.domain.orders.exceptions import (
    CatalogUnavailableError,
    InvalidQuantityError,
    ItemNotInCatalogError,
)


def test_place_order_stores_order_for_known_item(
    fake_orders: FakeOrderRepository, fake_catalog: FakeItemCatalog
) -> None:
    item_id = uuid4()
    fake_catalog.item_ids.add(item_id)

    order = PlaceOrder(fake_orders, fake_catalog).execute(item_id, 2)

    assert fake_orders.get(order.id) == order


def test_place_order_rejects_unknown_item(
    fake_orders: FakeOrderRepository, fake_catalog: FakeItemCatalog
) -> None:
    with pytest.raises(ItemNotInCatalogError):
        PlaceOrder(fake_orders, fake_catalog).execute(uuid4(), 1)
    assert fake_orders.orders == {}


def test_place_order_checks_quantity_before_calling_catalog(
    fake_orders: FakeOrderRepository, fake_catalog: FakeItemCatalog
) -> None:
    fake_catalog.is_available = False

    with pytest.raises(InvalidQuantityError):
        PlaceOrder(fake_orders, fake_catalog).execute(uuid4(), 0)


def test_place_order_propagates_catalog_outage(
    fake_orders: FakeOrderRepository, fake_catalog: FakeItemCatalog
) -> None:
    fake_catalog.is_available = False

    with pytest.raises(CatalogUnavailableError):
        PlaceOrder(fake_orders, fake_catalog).execute(uuid4(), 1)
    assert fake_orders.orders == {}
