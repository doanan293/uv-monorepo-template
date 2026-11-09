import json
from pathlib import Path

from import_worker.domain.imports.exceptions import InvalidBatchError


class FileInbox:
    """`Inbox` adapter over three directories: inbox, processed and failed.

    An import file is JSON shaped like `{"items": [{"name": "pen"}]}`.
    """

    def __init__(self, inbox_dir: Path, processed_dir: Path, failed_dir: Path) -> None:
        """Use these directories, creating any that are missing.

        Args:
            inbox_dir: Where new `*.json` files are dropped.
            processed_dir: Where imported files are moved.
            failed_dir: Where files that cannot be imported are moved.
        """
        self._inbox_dir = inbox_dir
        self._processed_dir = processed_dir
        self._failed_dir = failed_dir
        for directory in (inbox_dir, processed_dir, failed_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def list_pending(self) -> list[str]:
        """List `*.json` files in the inbox, sorted by name.

        Returns:
            File names.
        """
        return sorted(path.name for path in self._inbox_dir.glob("*.json"))

    def read_names(self, source: str) -> list[str]:
        """Read the item names of one file.

        Args:
            source: File name in the inbox.

        Returns:
            Item names as written in the file.

        Raises:
            InvalidBatchError: The file is not JSON of the expected shape.
        """
        text = (self._inbox_dir / source).read_text(encoding="utf-8")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise InvalidBatchError(source, "not valid JSON") from exc
        items = data.get("items") if isinstance(data, dict) else None
        if not isinstance(items, list):
            raise InvalidBatchError(source, 'expected {"items": [...]}')
        names = [item.get("name") for item in items if isinstance(item, dict)]
        if len(names) != len(items) or not all(isinstance(n, str) for n in names):
            raise InvalidBatchError(source, 'every item needs a string "name"')
        return [name for name in names if isinstance(name, str)]

    def mark_processed(self, source: str) -> None:
        """Move a file to the processed directory.

        Args:
            source: File name in the inbox.
        """
        (self._inbox_dir / source).replace(self._processed_dir / source)

    def mark_failed(self, source: str) -> None:
        """Move a file to the failed directory.

        Args:
            source: File name in the inbox.
        """
        (self._inbox_dir / source).replace(self._failed_dir / source)
