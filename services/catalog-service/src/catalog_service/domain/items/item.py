from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict

from catalog_service.domain.items.exceptions import InvalidItemNameError

MAX_NAME_LENGTH = 100


class Item(BaseModel):
    """A named item; immutable once created."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str
    created_at: datetime

    @classmethod
    def create(cls, name: str) -> Self:
        """Create a new item with a fresh id and the current UTC time.

        Args:
            name: Item name; surrounding whitespace is removed.

        Returns:
            The new item.

        Raises:
            InvalidItemNameError: The stripped name is empty or longer than
                `MAX_NAME_LENGTH` characters.
        """
        stripped = name.strip()
        if not 1 <= len(stripped) <= MAX_NAME_LENGTH:
            raise InvalidItemNameError
        return cls(id=uuid4(), name=stripped, created_at=datetime.now(UTC))
