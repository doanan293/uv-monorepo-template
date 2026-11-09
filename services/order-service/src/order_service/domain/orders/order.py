from datetime import UTC, datetime
from typing import Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict

from order_service.domain.orders.exceptions import InvalidQuantityError

MAX_QUANTITY = 1000


class Order(BaseModel):
    """An order for some quantity of one catalog item; immutable once created."""

    model_config = ConfigDict(frozen=True)

    id: UUID
    item_id: UUID
    quantity: int
    created_at: datetime

    @classmethod
    def create(cls, item_id: UUID, quantity: int) -> Self:
        """Create a new order with a fresh id and the current UTC time.

        Args:
            item_id: Catalog item being ordered.
            quantity: Number of units, from 1 to `MAX_QUANTITY`.

        Returns:
            The new order.

        Raises:
            InvalidQuantityError: The quantity is out of range.
        """
        if not 1 <= quantity <= MAX_QUANTITY:
            raise InvalidQuantityError
        return cls(
            id=uuid4(),
            item_id=item_id,
            quantity=quantity,
            created_at=datetime.now(UTC),
        )
