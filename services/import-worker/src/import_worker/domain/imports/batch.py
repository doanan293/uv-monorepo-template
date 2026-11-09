from typing import Self

from pydantic import BaseModel, ConfigDict

from import_worker.domain.imports.exceptions import InvalidBatchError

MAX_NAME_LENGTH = 100


class ItemBatch(BaseModel):
    """The item names read from one import file; immutable once created."""

    model_config = ConfigDict(frozen=True)

    source: str
    names: tuple[str, ...]

    @classmethod
    def create(cls, source: str, names: list[str]) -> Self:
        """Validate the names of one import file.

        Args:
            source: Name of the import file.
            names: Raw item names; surrounding whitespace is removed.

        Returns:
            The validated batch.

        Raises:
            InvalidBatchError: The file has no items, or a name is blank or
                longer than `MAX_NAME_LENGTH` characters.
        """
        if not names:
            raise InvalidBatchError(source, "no items")
        stripped = tuple(name.strip() for name in names)
        for name in stripped:
            if not 1 <= len(name) <= MAX_NAME_LENGTH:
                raise InvalidBatchError(source, "item names must be 1-100 characters")
        return cls(source=source, names=stripped)
