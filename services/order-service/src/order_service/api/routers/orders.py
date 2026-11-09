from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from order_service.api.dependencies import get_get_order, get_place_order
from order_service.api.schemas import OrderCreateRequest, OrderResponse
from order_service.application.orders.get_order import GetOrder
from order_service.application.orders.place_order import PlaceOrder

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Catalog is unavailable"}
    },
)
def place_order(
    body: OrderCreateRequest,
    use_case: Annotated[PlaceOrder, Depends(get_place_order)],
) -> OrderResponse:
    """Place an order.

    Returns `201` with the new order, `422` when the quantity is out of range
    or the item is not in the catalog, and `503` when the catalog is down.
    """
    order = use_case.execute(body.item_id, body.quantity)
    return OrderResponse.model_validate(order)


@router.get(
    "/{order_id}",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Unknown order"}},
)
def get_order(
    order_id: UUID,
    use_case: Annotated[GetOrder, Depends(get_get_order)],
) -> OrderResponse:
    """Return one order, or `404` when no order has this id."""
    return OrderResponse.model_validate(use_case.execute(order_id))
