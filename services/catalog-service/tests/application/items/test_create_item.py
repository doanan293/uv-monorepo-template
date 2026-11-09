from catalog_service.application.items.create_item import CreateItem
from catalog_service.domain.items.repository import ItemRepository


def test_create_item_stores_item(fake_repository: ItemRepository) -> None:
    item = CreateItem(fake_repository).execute("pen")

    assert item.name == "pen"
    assert fake_repository.get(item.id) == item
