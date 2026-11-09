"""Composition root: the only place in `api` that builds `infra` adapters."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from catalog_service.application.items.create_item import CreateItem
from catalog_service.application.items.get_item import GetItem
from catalog_service.infra.memory.item_repository import InMemoryItemRepository


@lru_cache
def get_item_repository() -> InMemoryItemRepository:
    """Return the process-wide item repository.

    Cached so items persist across requests.
    """
    return InMemoryItemRepository()


Repository = Annotated[InMemoryItemRepository, Depends(get_item_repository)]


def get_create_item(repository: Repository) -> CreateItem:
    """Build the create-item use case for one request."""
    return CreateItem(repository)


def get_get_item(repository: Repository) -> GetItem:
    """Build the get-item use case for one request."""
    return GetItem(repository)
