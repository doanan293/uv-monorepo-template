from uuid import UUID

from catalog_service.shared.exceptions import InvalidInputError, NotFoundError


class ItemNotFoundError(NotFoundError):
    """No item exists with the requested id."""

    def __init__(self, item_id: UUID) -> None:
        """Build the error for one missing item.

        Args:
            item_id: Id that was looked up.
        """
        super().__init__(f"Item {item_id} not found")
        self.item_id = item_id


class InvalidItemNameError(InvalidInputError):
    """An item name is blank or longer than the allowed maximum."""

    def __init__(self) -> None:
        """Build the error with the name rule in its message."""
        super().__init__("Item name must be 1-100 characters")
