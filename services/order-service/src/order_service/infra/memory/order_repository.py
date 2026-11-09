from uuid import UUID

from order_service.domain.orders.order import Order


class InMemoryOrderRepository:
    """`OrderRepository` adapter that keeps orders in process memory.

    Data is lost on restart; replace it with a database adapter in a real
    service.
    """

    def __init__(self) -> None:
        """Start with no orders."""
        self._orders: dict[UUID, Order] = {}

    def add(self, order: Order) -> None:
        """Store a new order.

        Args:
            order: Order to store.
        """
        self._orders[order.id] = order

    def get(self, order_id: UUID) -> Order | None:
        """Load an order by id.

        Args:
            order_id: Id of the order.

        Returns:
            The order, or `None` when no order has this id.
        """
        return self._orders.get(order_id)
