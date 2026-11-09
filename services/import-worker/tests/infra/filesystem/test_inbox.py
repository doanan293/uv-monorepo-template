import json
from pathlib import Path

import pytest

from import_worker.domain.imports.exceptions import InvalidBatchError
from import_worker.infra.filesystem.inbox import FileInbox


@pytest.fixture
def inbox(tmp_path: Path) -> FileInbox:
    return FileInbox(tmp_path / "inbox", tmp_path / "processed", tmp_path / "failed")


def _write(tmp_path: Path, name: str, content: str) -> None:
    (tmp_path / "inbox" / name).write_text(content, encoding="utf-8")


def test_creates_missing_directories(tmp_path: Path, inbox: FileInbox) -> None:
    for directory in ("inbox", "processed", "failed"):
        assert (tmp_path / directory).is_dir()


def test_list_pending_returns_sorted_json_files(
    tmp_path: Path, inbox: FileInbox
) -> None:
    _write(tmp_path, "b.json", "{}")
    _write(tmp_path, "a.json", "{}")
    _write(tmp_path, "notes.txt", "")

    assert inbox.list_pending() == ["a.json", "b.json"]


def test_read_names_parses_items(tmp_path: Path, inbox: FileInbox) -> None:
    _write(tmp_path, "a.json", json.dumps({"items": [{"name": "pen"}]}))

    assert inbox.read_names("a.json") == ["pen"]


@pytest.mark.parametrize(
    "content",
    ["not json", "[]", '{"items": "pen"}', '{"items": [{"title": "pen"}]}'],
)
def test_read_names_rejects_malformed_file(
    tmp_path: Path, inbox: FileInbox, content: str
) -> None:
    _write(tmp_path, "a.json", content)

    with pytest.raises(InvalidBatchError):
        inbox.read_names("a.json")


def test_mark_processed_and_failed_move_files(tmp_path: Path, inbox: FileInbox) -> None:
    _write(tmp_path, "a.json", "{}")
    _write(tmp_path, "b.json", "{}")

    inbox.mark_processed("a.json")
    inbox.mark_failed("b.json")

    assert (tmp_path / "processed" / "a.json").exists()
    assert (tmp_path / "failed" / "b.json").exists()
    assert inbox.list_pending() == []
