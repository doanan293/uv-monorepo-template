import logging

from import_worker.shared.settings import get_settings
from import_worker.worker.runner import build_use_case, run


def main() -> None:
    """Configure logging and poll the inbox until the process is stopped."""
    settings = get_settings()
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    logging.getLogger(__name__).info("Watching %s", settings.inbox_dir.resolve())
    run(build_use_case(settings), settings.poll_interval_seconds)
