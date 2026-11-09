from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from catalog_service.api.dependencies import get_create_item, get_get_item
from catalog_service.api.schemas import ItemCreateRequest, ItemResponse
from catalog_service.application.items.create_item import CreateItem
from catalog_service.application.items.get_item import GetItem

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_item(
    body: ItemCreateRequest,
    use_case: Annotated[CreateItem, Depends(get_create_item)],
) -> ItemResponse:
    """Create an item.

    Returns `201` with the new item, or `422` when the name is blank or
    longer than 100 characters.
    """
    return ItemResponse.model_validate(use_case.execute(body.name))


@router.get(
    "/{item_id}", responses={status.HTTP_404_NOT_FOUND: {"description": "Unknown item"}}
)
def get_item(
    item_id: UUID,
    use_case: Annotated[GetItem, Depends(get_get_item)],
) -> ItemResponse:
    """Return one item, or `404` when no item has this id."""
    return ItemResponse.model_validate(use_case.execute(item_id))
