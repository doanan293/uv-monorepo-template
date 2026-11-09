"""Composition root and polling loop of the worker."""

import logging
import time
from collections.abc import Callable
from typing import Protocol

import httpx2

from import_worker.application.imports.import_pending_files import (
    ImportPendingFiles,
    ImportReport,
)
from import_worker.infra.catalog_http.item_catalog import HttpItemCatalog
from import_worker.infra.filesystem.inbox import FileInbox
from import_worker.shared.exceptions import ServiceUnavailableError
from import_worker.shared.settings import Settings

logger = logging.getLogger(__name__)


class ImportUseCase(Protocol):
    """What the loop needs from the import use case."""

    def execute(self) -> ImportReport:
        """Run one import pass."""
        ...


def build_use_case(settings: Settings) -> ImportPendingFiles:
    """Build the import use case with its real adapters.

    Args:
        settings: Directories, catalog URL and timeout.

    Returns:
        The wired use case.
    """
    inbox = FileInbox(settings.inbox_dir, settings.processed_dir, settings.failed_dir)
    client = httpx2.Client(
        base_url=settings.catalog_url, timeout=settings.catalog_timeout_seconds
    )
    return ImportPendingFiles(inbox, HttpItemCatalog(client))


def run(
    use_case: ImportUseCase,
    poll_interval_seconds: float,
    sleep: Callable[[float], None] = time.sleep,
    max_iterations: int | None = None,
) -> None:
    """Run import passes forever (or `max_iterations` times), sleeping between.

    An unavailable catalog is logged and retried on the next pass.

    Args:
        use_case: The import use case.
        poll_interval_seconds: Pause after each pass.
        sleep: Sleep function; replaced in tests.
        max_iterations: Stop after this many passes; `None` runs forever.
    """
    iteration = 0
    while max_iterations is None or iteration < max_iterations:
        try:
            report = use_case.execute()
        except ServiceUnavailableError as exc:
            logger.warning("%s; retrying in %ss", exc, poll_interval_seconds)
        else:
            if report.processed or report.failed:
                logger.info(
                    "Imported %d file(s), %d failed", report.processed, report.failed
                )
        iteration += 1
        sleep(poll_interval_seconds)
