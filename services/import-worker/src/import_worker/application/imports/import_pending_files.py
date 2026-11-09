import logging

from pydantic import BaseModel

from import_worker.domain.imports.batch import ItemBatch
from import_worker.domain.imports.inbox import Inbox
from import_worker.domain.imports.item_catalog import ItemCatalog
from import_worker.shared.exceptions import InvalidInputError

logger = logging.getLogger(__name__)


class ImportReport(BaseModel):
    """Outcome of one pass over the inbox."""

    processed: int
    failed: int


class ImportPendingFiles:
    """Use case: import every pending file in the inbox into the catalog."""

    def __init__(self, inbox: Inbox, catalog: ItemCatalog) -> None:
        """Wire the use case to its ports.

        Args:
            inbox: Where import files wait.
            catalog: Where items are created.
        """
        self._inbox = inbox
        self._catalog = catalog

    def execute(self) -> ImportReport:
        """Import each pending file; move bad files aside and keep going.

        A file whose items were all created is marked processed. A file that is
        malformed, or holds an item the catalog rejects, is marked failed.

        Returns:
            How many files were processed and how many failed.

        Raises:
            CatalogUnavailableError: The catalog is down; the current file stays
                in the inbox and is retried on the next pass. Items already
                created from it are created again on retry.
        """
        processed = failed = 0
        for source in self._inbox.list_pending():
            try:
                self._import_file(source)
            except InvalidInputError as exc:
                logger.warning("Import failed: %s", exc)
                self._inbox.mark_failed(source)
                failed += 1
            else:
                self._inbox.mark_processed(source)
                processed += 1
        return ImportReport(processed=processed, failed=failed)

    def _import_file(self, source: str) -> None:
        batch = ItemBatch.create(source, self._inbox.read_names(source))
        for name in batch.names:
            self._catalog.create_item(name)
