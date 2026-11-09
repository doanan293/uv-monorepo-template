from uuid import uuid4

import pytest

from catalog_service.application.items.get_item import GetItem
from catalog_service.domain.items.exceptions import ItemNotFoundError
from catalog_service.domain.items.item import Item
from catalog_service.domain.items.repository import ItemRepository


def test_get_item_returns_stored_item(fake_repository: ItemRepository) -> None:
    item = Item.create("pen")
    fake_repository.add(item)

    assert GetItem(fake_repository).execute(item.id) == item


def test_get_item_raises_when_missing(fake_repository: ItemRepository) -> None:
    with pytest.raises(ItemNotFoundError):
        GetItem(fake_repository).execute(uuid4())
