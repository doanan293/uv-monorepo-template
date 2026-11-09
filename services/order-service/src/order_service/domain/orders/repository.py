from typing import Protocol
from uuid import UUID

from order_service.domain.orders.order import Order


class OrderRepository(Protocol):
    """Port for storing and loading orders; implemented in `infra`."""

    def add(self, order: Order) -> None:
        """Store a new order.

        Args:
            order: Order to store.
        """
        ...

    def get(self, order_id: UUID) -> Order | None:
        """Load an order by id.

        Args:
            order_id: Id of the order.

        Returns:
            The order, or `None` when no order has this id.
        """
        ...
