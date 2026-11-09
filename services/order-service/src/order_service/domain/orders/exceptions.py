from uuid import UUID

from order_service.shared.exceptions import (
    InvalidInputError,
    NotFoundError,
    ServiceUnavailableError,
)


class OrderNotFoundError(NotFoundError):
    """No order exists with the requested id."""

    def __init__(self, order_id: UUID) -> None:
        """Build the error for one missing order.

        Args:
            order_id: Id that was looked up.
        """
        super().__init__(f"Order {order_id} not found")
        self.order_id = order_id


class InvalidQuantityError(InvalidInputError):
    """An order quantity is outside the allowed range."""

    def __init__(self) -> None:
        """Build the error with the quantity rule in its message."""
        super().__init__("Quantity must be between 1 and 1000")


class ItemNotInCatalogError(InvalidInputError):
    """An order refers to an item the catalog does not know."""

    def __init__(self, item_id: UUID) -> None:
        """Build the error for one unknown item.

        Args:
            item_id: Item the order referred to.
        """
        super().__init__(f"Item {item_id} is not in the catalog")
        self.item_id = item_id


class CatalogUnavailableError(ServiceUnavailableError):
    """The catalog could not be asked whether an item exists."""

    def __init__(self) -> None:
        """Build the error with a fixed message."""
        super().__init__("Catalog service is unavailable")
