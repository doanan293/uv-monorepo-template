from typing import Protocol
from uuid import UUID

from catalog_service.domain.items.item import Item


class ItemRepository(Protocol):
    """Port for storing and loading items; implemented in `infra`."""

    def add(self, item: Item) -> None:
        """Store a new item.

        Args:
            item: Item to store.
        """
        ...

    def get(self, item_id: UUID) -> Item | None:
        """Load an item by id.

        Args:
            item_id: Id of the item.

        Returns:
            The item, or `None` when no item has this id.
        """
        ...
