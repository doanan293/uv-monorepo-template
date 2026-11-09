import httpx2

from import_worker.domain.imports.exceptions import (
    CatalogUnavailableError,
    ItemRejectedError,
)


class HttpItemCatalog:
    """`ItemCatalog` adapter that calls catalog-service over HTTP."""

    def __init__(self, client: httpx2.Client) -> None:
        """Use a client whose `base_url` points at catalog-service.

        Args:
            client: HTTP client; owns the base URL and timeout.
        """
        self._client = client

    def create_item(self, name: str) -> None:
        """Create an item with `POST /api/v1/items`.

        Args:
            name: Item name.

        Raises:
            ItemRejectedError: The catalog answered `422`.
            CatalogUnavailableError: Any other non-`201` status, or the request
                failed.
        """
        try:
            response = self._client.post("/api/v1/items", json={"name": name})
        except httpx2.HTTPError as exc:
            raise CatalogUnavailableError from exc
        if response.status_code == httpx2.codes.CREATED:
            return
        if response.status_code == httpx2.codes.UNPROCESSABLE_CONTENT:
            raise ItemRejectedError(name)
        raise CatalogUnavailableError
