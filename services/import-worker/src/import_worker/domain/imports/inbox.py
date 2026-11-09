from typing import Protocol


class Inbox(Protocol):
    """Port for import files waiting to be processed; implemented in `infra`."""

    def list_pending(self) -> list[str]:
        """List files waiting to be imported, oldest name first.

        Returns:
            File names, in a stable order.
        """
        ...

    def read_names(self, source: str) -> list[str]:
        """Read the raw item names of one file.

        Args:
            source: File name from `list_pending`.

        Returns:
            Item names as written in the file.

        Raises:
            InvalidBatchError: The file is not in the expected format.
        """
        ...

    def mark_processed(self, source: str) -> None:
        """Move a file out of the inbox after a successful import.

        Args:
            source: File name from `list_pending`.
        """
        ...

    def mark_failed(self, source: str) -> None:
        """Move a file out of the inbox because it cannot be imported.

        Args:
            source: File name from `list_pending`.
        """
        ...
