from uuid import uuid4

import pytest

from fakes import FakeOrderRepository
from order_service.application.orders.get_order import GetOrder
from order_service.domain.orders.exceptions import OrderNotFoundError
from order_service.domain.orders.order import Order


def test_get_order_returns_stored_order(fake_orders: FakeOrderRepository) -> None:
    order = Order.create(uuid4(), 1)
    fake_orders.add(order)

    assert GetOrder(fake_orders).execute(order.id) == order


def test_get_order_raises_when_missing(fake_orders: FakeOrderRepository) -> None:
    with pytest.raises(OrderNotFoundError):
        GetOrder(fake_orders).execute(uuid4())
