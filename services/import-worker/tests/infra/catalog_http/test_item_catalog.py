import json

import httpx2
import pytest

from import_worker.domain.imports.exceptions import (
    CatalogUnavailableError,
    ItemRejectedError,
)
from import_worker.infra.catalog_http.item_catalog import HttpItemCatalog


def _catalog(transport: httpx2.MockTransport) -> HttpItemCatalog:
    return HttpItemCatalog(
        httpx2.Client(base_url="http://catalog", transport=transport)
    )


def test_create_item_posts_name() -> None:
    requests: list[httpx2.Request] = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        return httpx2.Response(201, json={})

    _catalog(httpx2.MockTransport(handler)).create_item("pen")

    assert requests[0].method == "POST"
    assert requests[0].url.path == "/api/v1/items"
    assert json.loads(requests[0].content) == {"name": "pen"}


def test_create_item_raises_rejected_on_422() -> None:
    transport = httpx2.MockTransport(lambda _: httpx2.Response(422))

    with pytest.raises(ItemRejectedError):
        _catalog(transport).create_item("pen")


def test_create_item_raises_unavailable_on_server_error() -> None:
    transport = httpx2.MockTransport(lambda _: httpx2.Response(503))

    with pytest.raises(CatalogUnavailableError):
        _catalog(transport).create_item("pen")


def test_create_item_raises_unavailable_when_unreachable() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("refused", request=request)

    with pytest.raises(CatalogUnavailableError):
        _catalog(httpx2.MockTransport(handler)).create_item("pen")
