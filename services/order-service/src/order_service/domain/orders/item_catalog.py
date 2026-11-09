from typing import Protocol
from uuid import UUID


class ItemCatalog(Protocol):
    """Port for asking the catalog about items; implemented in `infra`."""

    def has_item(self, item_id: UUID) -> bool:
        """Tell whether the catalog knows an item.

        Args:
            item_id: Id of the item.

        Returns:
            `True` when the item exists.

        Raises:
            CatalogUnavailableError: The catalog cannot answer.
        """
        ...
