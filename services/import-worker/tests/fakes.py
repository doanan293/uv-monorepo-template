from import_worker.domain.imports.exceptions import (
    CatalogUnavailableError,
    InvalidBatchError,
    ItemRejectedError,
)


class FakeInbox:
    """Test double for `Inbox`: files are a dict of source -> names (or None)."""

    def __init__(self, files: dict[str, list[str] | None]) -> None:
        self.files = files
        self.processed: list[str] = []
        self.failed: list[str] = []

    def list_pending(self) -> list[str]:
        done = set(self.processed) | set(self.failed)
        return [source for source in sorted(self.files) if source not in done]

    def read_names(self, source: str) -> list[str]:
        names = self.files[source]
        if names is None:
            raise InvalidBatchError(source, "not valid JSON")
        return names

    def mark_processed(self, source: str) -> None:
        self.processed.append(source)

    def mark_failed(self, source: str) -> None:
        self.failed.append(source)


class FakeItemCatalog:
    """Test double for `ItemCatalog` that records created names."""

    def __init__(self, rejected: set[str] | None = None) -> None:
        self.created: list[str] = []
        self.rejected = rejected or set()
        self.is_available = True

    def create_item(self, name: str) -> None:
        if not self.is_available:
            raise CatalogUnavailableError
        if name in self.rejected:
            raise ItemRejectedError(name)
        self.created.append(name)
