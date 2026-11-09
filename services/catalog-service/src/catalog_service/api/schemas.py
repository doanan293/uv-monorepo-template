from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ItemCreateRequest(BaseModel):
    """Body of `POST /api/v1/items`."""

    model_config = ConfigDict(json_schema_extra={"examples": [{"name": "pen"}]})

    name: str


class ItemResponse(BaseModel):
    """An item as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    created_at: datetime
