"""Composition root: the only place in `api` that builds `infra` adapters."""

from functools import lru_cache
from typing import Annotated

import httpx2
from fastapi import Depends

from order_service.application.orders.get_order import GetOrder
from order_service.application.orders.place_order import PlaceOrder
from order_service.infra.catalog_http.item_catalog import HttpItemCatalog
from order_service.infra.memory.order_repository import InMemoryOrderRepository
from order_service.shared.settings import get_settings


@lru_cache
def get_order_repository() -> InMemoryOrderRepository:
    """Return the process-wide order repository.

    Cached so orders persist across requests.
    """
    return InMemoryOrderRepository()


@lru_cache
def get_item_catalog() -> HttpItemCatalog:
    """Return the process-wide catalog client.

    Cached so every request reuses one HTTP connection pool.
    """
    settings = get_settings()
    client = httpx2.Client(
        base_url=settings.catalog_url, timeout=settings.catalog_timeout_seconds
    )
    return HttpItemCatalog(client)


Orders = Annotated[InMemoryOrderRepository, Depends(get_order_repository)]
Catalog = Annotated[HttpItemCatalog, Depends(get_item_catalog)]


def get_place_order(orders: Orders, catalog: Catalog) -> PlaceOrder:
    """Build the place-order use case for one request."""
    return PlaceOrder(orders, catalog)


def get_get_order(orders: Orders) -> GetOrder:
    """Build the get-order use case for one request."""
    return GetOrder(orders)
