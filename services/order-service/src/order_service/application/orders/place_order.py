from uuid import UUID

from order_service.domain.orders.exceptions import ItemNotInCatalogError
from order_service.domain.orders.item_catalog import ItemCatalog
from order_service.domain.orders.order import Order
from order_service.domain.orders.repository import OrderRepository


class PlaceOrder:
    """Use case: place an order for an item the catalog knows."""

    def __init__(self, orders: OrderRepository, catalog: ItemCatalog) -> None:
        """Wire the use case to its ports.

        Args:
            orders: Where orders are stored.
            catalog: Where items are looked up.
        """
        self._orders = orders
        self._catalog = catalog

    def execute(self, item_id: UUID, quantity: int) -> Order:
        """Validate, check the catalog, then store the order.

        Args:
            item_id: Catalog item being ordered.
            quantity: Number of units.

        Returns:
            The stored order.

        Raises:
            InvalidQuantityError: The quantity is out of range.
            ItemNotInCatalogError: The catalog does not know the item.
            CatalogUnavailableError: The catalog cannot answer.
        """
        order = Order.create(item_id, quantity)
        if not self._catalog.has_item(item_id):
            raise ItemNotInCatalogError(item_id)
        self._orders.add(order)
        return order
