from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrderCreateRequest(BaseModel):
    """Body of `POST /api/v1/orders`."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"item_id": "1b0ce4ef-3055-4f49-8743-fb19833a6dc1", "quantity": 2}
            ]
        }
    )

    item_id: UUID
    quantity: int


class OrderResponse(BaseModel):
    """An order as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    item_id: UUID
    quantity: int
    created_at: datetime
