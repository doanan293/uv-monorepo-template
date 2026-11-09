from catalog_service.domain.items.item import Item
from catalog_service.domain.items.repository import ItemRepository


class CreateItem:
    """Use case: create and store a new item."""

    def __init__(self, repository: ItemRepository) -> None:
        """Wire the use case to its storage port.

        Args:
            repository: Where items are stored.
        """
        self._repository = repository

    def execute(self, name: str) -> Item:
        """Create an item and store it.

        Args:
            name: Item name.

        Returns:
            The stored item.

        Raises:
            InvalidItemNameError: The name breaks the item name rule.
        """
        item = Item.create(name)
        self._repository.add(item)
        return item
