from uuid import UUID

from catalog_service.domain.items.exceptions import ItemNotFoundError
from catalog_service.domain.items.item import Item
from catalog_service.domain.items.repository import ItemRepository


class GetItem:
    """Use case: load one item by id."""

    def __init__(self, repository: ItemRepository) -> None:
        """Wire the use case to its storage port.

        Args:
            repository: Where items are stored.
        """
        self._repository = repository

    def execute(self, item_id: UUID) -> Item:
        """Load an item.

        Args:
            item_id: Id of the item.

        Returns:
            The item.

        Raises:
            ItemNotFoundError: No item has this id.
        """
        item = self._repository.get(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        return item
