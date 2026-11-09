from uuid import uuid4

import httpx2
import pytest

from order_service.domain.orders.exceptions import CatalogUnavailableError
from order_service.infra.catalog_http.item_catalog import HttpItemCatalog


def _catalog(handler: httpx2.MockTransport) -> HttpItemCatalog:
    return HttpItemCatalog(httpx2.Client(base_url="http://catalog", transport=handler))


def test_has_item_calls_catalog_items_endpoint() -> None:
    item_id = uuid4()
    seen: list[str] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen.append(request.url.path)
        return httpx2.Response(200, json={"id": str(item_id)})

    assert _catalog(httpx2.MockTransport(handler)).has_item(item_id) is True
    assert seen == [f"/api/v1/items/{item_id}"]


def test_has_item_is_false_on_404() -> None:
    transport = httpx2.MockTransport(lambda _: httpx2.Response(404))

    assert _catalog(transport).has_item(uuid4()) is False


def test_has_item_raises_on_server_error() -> None:
    transport = httpx2.MockTransport(lambda _: httpx2.Response(500))

    with pytest.raises(CatalogUnavailableError):
        _catalog(transport).has_item(uuid4())


def test_has_item_raises_when_catalog_unreachable() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("refused", request=request)

    with pytest.raises(CatalogUnavailableError):
        _catalog(httpx2.MockTransport(handler)).has_item(uuid4())
