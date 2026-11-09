import uvicorn

from catalog_service.api.app import create_app
from catalog_service.shared.settings import get_settings


def main() -> None:
    """Run the HTTP server with the configured host, port and log level."""
    settings = get_settings()
    uvicorn.run(
        create_app(),
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
    )
