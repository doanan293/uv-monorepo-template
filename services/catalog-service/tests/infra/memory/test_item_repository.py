from uuid import uuid4

from catalog_service.domain.items.item import Item
from catalog_service.infra.memory.item_repository import InMemoryItemRepository


def test_get_returns_added_item() -> None:
    repository = InMemoryItemRepository()
    item = Item.create("pen")

    repository.add(item)

    assert repository.get(item.id) == item


def test_get_returns_none_for_unknown_id() -> None:
    assert InMemoryItemRepository().get(uuid4()) is None
