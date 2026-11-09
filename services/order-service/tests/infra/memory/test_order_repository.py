from uuid import uuid4

from order_service.domain.orders.order import Order
from order_service.infra.memory.order_repository import InMemoryOrderRepository


def test_get_returns_added_order() -> None:
    repository = InMemoryOrderRepository()
    order = Order.create(uuid4(), 1)

    repository.add(order)

    assert repository.get(order.id) == order


def test_get_returns_none_for_unknown_id() -> None:
    assert InMemoryOrderRepository().get(uuid4()) is None
