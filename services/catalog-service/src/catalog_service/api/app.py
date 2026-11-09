from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from catalog_service.api.routers import health, items
from catalog_service.shared.exceptions import InvalidInputError, NotFoundError


def _not_found_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse({"detail": str(exc)}, status_code=status.HTTP_404_NOT_FOUND)


def _invalid_input_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        {"detail": str(exc)}, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
    )


def create_app() -> FastAPI:
    """Build the FastAPI application with its routers and error handlers.

    Returns:
        The configured application.
    """
    app = FastAPI(title="catalog-service")
    app.include_router(health.router)
    app.include_router(items.router)
    app.add_exception_handler(NotFoundError, _not_found_handler)
    app.add_exception_handler(InvalidInputError, _invalid_input_handler)
    return app
