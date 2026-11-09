from uuid import UUID, uuid4

import pytest

from order_service.domain.orders.exceptions import InvalidQuantityError
from order_service.domain.orders.order import Order


def test_create_sets_fields() -> None:
    item_id = uuid4()

    order = Order.create(item_id, 3)

    assert order.item_id == item_id
    assert order.quantity == 3
    assert isinstance(order.id, UUID)
    assert order.created_at.tzinfo is not None


@pytest.mark.parametrize("quantity", [0, -1, 1001])
def test_create_rejects_quantity_out_of_range(quantity: int) -> None:
    with pytest.raises(InvalidQuantityError):
        Order.create(uuid4(), quantity)


@pytest.mark.parametrize("quantity", [1, 1000])
def test_create_accepts_quantity_bounds(quantity: int) -> None:
    assert Order.create(uuid4(), quantity).quantity == quantity
