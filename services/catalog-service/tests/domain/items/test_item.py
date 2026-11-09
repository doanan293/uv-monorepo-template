from uuid import UUID

import pytest
from pydantic import ValidationError

from catalog_service.domain.items.exceptions import InvalidItemNameError
from catalog_service.domain.items.item import Item


def test_create_strips_name() -> None:
    item = Item.create("  pen  ")

    assert item.name == "pen"
    assert isinstance(item.id, UUID)
    assert item.created_at.tzinfo is not None


@pytest.mark.parametrize("name", ["", "   "])
def test_create_rejects_blank_name(name: str) -> None:
    with pytest.raises(InvalidItemNameError):
        Item.create(name)


def test_create_rejects_too_long_name() -> None:
    assert Item.create("x" * 100).name == "x" * 100
    with pytest.raises(InvalidItemNameError):
        Item.create("x" * 101)


@pytest.mark.parametrize("field", ["id", "name", "created_at"])
def test_item_is_immutable(field: str) -> None:
    item = Item.create("pen")

    with pytest.raises(ValidationError):
        setattr(item, field, "changed")
