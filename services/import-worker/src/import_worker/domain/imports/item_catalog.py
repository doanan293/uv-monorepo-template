from typing import Protocol


class ItemCatalog(Protocol):
    """Port for creating items in the catalog; implemented in `infra`."""

    def create_item(self, name: str) -> None:
        """Create one item.

        Args:
            name: Item name.

        Raises:
            ItemRejectedError: The catalog refused the item.
            CatalogUnavailableError: The catalog cannot be reached.
        """
        ...
