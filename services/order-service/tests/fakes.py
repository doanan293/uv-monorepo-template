from uuid import UUID

from order_service.domain.orders.exceptions import CatalogUnavailableError
from order_service.domain.orders.order import Order


class FakeOrderRepository:
    """Test double for `OrderRepository` that exposes what was stored."""

    def __init__(self) -> None:
        self.orders: dict[UUID, Order] = {}

    def add(self, order: Order) -> None:
        self.orders[order.id] = order

    def get(self, order_id: UUID) -> Order | None:
        return self.orders.get(order_id)


class FakeItemCatalog:
    """Test double for `ItemCatalog` with a fixed set of known items."""

    def __init__(self, item_ids: set[UUID] | None = None) -> None:
        self.item_ids = item_ids or set()
        self.is_available = True

    def has_item(self, item_id: UUID) -> bool:
        if not self.is_available:
            raise CatalogUnavailableError
        return item_id in self.item_ids
