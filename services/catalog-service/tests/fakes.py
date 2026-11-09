from uuid import UUID

from catalog_service.domain.items.item import Item


class FakeItemRepository:
    """Test double for `ItemRepository` that exposes what was stored."""

    def __init__(self) -> None:
        self.items: dict[UUID, Item] = {}

    def add(self, item: Item) -> None:
        self.items[item.id] = item

    def get(self, item_id: UUID) -> Item | None:
        return self.items.get(item_id)
