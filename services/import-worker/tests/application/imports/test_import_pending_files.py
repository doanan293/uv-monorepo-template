import pytest

from fakes import FakeInbox, FakeItemCatalog
from import_worker.application.imports.import_pending_files import (
    ImportPendingFiles,
    ImportReport,
)
from import_worker.domain.imports.exceptions import CatalogUnavailableError


def test_imports_every_valid_file() -> None:
    inbox = FakeInbox({"a.json": ["pen"], "b.json": ["book", "cup"]})
    catalog = FakeItemCatalog()

    report = ImportPendingFiles(inbox, catalog).execute()

    assert report == ImportReport(processed=2, failed=0)
    assert catalog.created == ["pen", "book", "cup"]
    assert inbox.processed == ["a.json", "b.json"]


def test_moves_invalid_file_to_failed_and_continues() -> None:
    inbox = FakeInbox({"a.json": None, "b.json": [" "], "c.json": ["pen"]})
    catalog = FakeItemCatalog()

    report = ImportPendingFiles(inbox, catalog).execute()

    assert report == ImportReport(processed=1, failed=2)
    assert inbox.failed == ["a.json", "b.json"]
    assert catalog.created == ["pen"]


def test_marks_file_failed_when_catalog_rejects_an_item() -> None:
    inbox = FakeInbox({"a.json": ["pen"]})

    report = ImportPendingFiles(inbox, FakeItemCatalog(rejected={"pen"})).execute()

    assert report == ImportReport(processed=0, failed=1)
    assert inbox.failed == ["a.json"]


def test_leaves_file_pending_when_catalog_is_down() -> None:
    inbox = FakeInbox({"a.json": ["pen"]})
    catalog = FakeItemCatalog()
    catalog.is_available = False

    with pytest.raises(CatalogUnavailableError):
        ImportPendingFiles(inbox, catalog).execute()
    assert inbox.list_pending() == ["a.json"]


def test_empty_inbox_reports_nothing() -> None:
    report = ImportPendingFiles(FakeInbox({}), FakeItemCatalog()).execute()

    assert report == ImportReport(processed=0, failed=0)
