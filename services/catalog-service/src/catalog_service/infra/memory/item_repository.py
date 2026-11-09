from uuid import UUID

from catalog_service.domain.items.item import Item


class InMemoryItemRepository:
    """`ItemRepository` adapter that keeps items in process memory.

    Data is lost on restart; replace it with a database adapter in a real
    service.
    """

    def __init__(self) -> None:
        """Start with no items."""
        self._items: dict[UUID, Item] = {}

    def add(self, item: Item) -> None:
        """Store a new item.

        Args:
            item: Item to store.
        """
        self._items[item.id] = item

    def get(self, item_id: UUID) -> Item | None:
        """Load an item by id.

        Args:
            item_id: Id of the item.

        Returns:
            The item, or `None` when no item has this id.
        """
        return self._items.get(item_id)
