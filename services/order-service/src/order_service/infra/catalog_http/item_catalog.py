from uuid import UUID

import httpx2

from order_service.domain.orders.exceptions import CatalogUnavailableError


class HttpItemCatalog:
    """`ItemCatalog` adapter that calls catalog-service over HTTP."""

    def __init__(self, client: httpx2.Client) -> None:
        """Use a client whose `base_url` points at catalog-service.

        Args:
            client: HTTP client; owns the base URL and timeout.
        """
        self._client = client

    def has_item(self, item_id: UUID) -> bool:
        """Ask `GET /api/v1/items/{item_id}` whether the item exists.

        Args:
            item_id: Id of the item.

        Returns:
            `True` on `200`, `False` on `404`.

        Raises:
            CatalogUnavailableError: Any other status, or the request failed.
        """
        try:
            response = self._client.get(f"/api/v1/items/{item_id}")
        except httpx2.HTTPError as exc:
            raise CatalogUnavailableError from exc
        if response.status_code == httpx2.codes.OK:
            return True
        if response.status_code == httpx2.codes.NOT_FOUND:
            return False
        raise CatalogUnavailableError
