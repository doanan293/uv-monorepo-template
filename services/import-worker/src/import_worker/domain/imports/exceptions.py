from import_worker.shared.exceptions import InvalidInputError, ServiceUnavailableError


class InvalidBatchError(InvalidInputError):
    """An import file cannot be turned into a valid batch of items."""

    def __init__(self, source: str, reason: str) -> None:
        """Build the error for one bad file.

        Args:
            source: Name of the import file.
            reason: What is wrong with it.
        """
        super().__init__(f"{source}: {reason}")
        self.source = source


class ItemRejectedError(InvalidInputError):
    """The catalog refused to create an item."""

    def __init__(self, name: str) -> None:
        """Build the error for one refused item.

        Args:
            name: Item name the catalog refused.
        """
        super().__init__(f"Catalog rejected item {name!r}")
        self.name = name


class CatalogUnavailableError(ServiceUnavailableError):
    """The catalog could not be reached; the import should be retried later."""

    def __init__(self) -> None:
        """Build the error with a fixed message."""
        super().__init__("Catalog service is unavailable")
