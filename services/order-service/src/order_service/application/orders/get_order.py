from uuid import UUID

from order_service.domain.orders.exceptions import OrderNotFoundError
from order_service.domain.orders.order import Order
from order_service.domain.orders.repository import OrderRepository


class GetOrder:
    """Use case: load one order by id."""

    def __init__(self, orders: OrderRepository) -> None:
        """Wire the use case to its storage port.

        Args:
            orders: Where orders are stored.
        """
        self._orders = orders

    def execute(self, order_id: UUID) -> Order:
        """Load an order.

        Args:
            order_id: Id of the order.

        Returns:
            The order.

        Raises:
            OrderNotFoundError: No order has this id.
        """
        order = self._orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order
