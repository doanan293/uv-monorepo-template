from collections.abc import Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from order_service.api.routers import health, orders
from order_service.shared.exceptions import (
    InvalidInputError,
    NotFoundError,
    ServiceUnavailableError,
)

_STATUS_BY_ERROR: dict[type[Exception], int] = {
    NotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidInputError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ServiceUnavailableError: status.HTTP_503_SERVICE_UNAVAILABLE,
}


def _error_handler(status_code: int) -> Callable[[Request, Exception], JSONResponse]:
    def handle(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse({"detail": str(exc)}, status_code=status_code)

    return handle


def create_app() -> FastAPI:
    """Build the FastAPI application with its routers and error handlers.

    Returns:
        The configured application.
    """
    app = FastAPI(title="order-service")
    app.include_router(health.router)
    app.include_router(orders.router)
    for error, status_code in _STATUS_BY_ERROR.items():
        app.add_exception_handler(error, _error_handler(status_code))
    return app
