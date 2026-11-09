from pathlib import Path

import pytest

from import_worker.application.imports.import_pending_files import ImportReport
from import_worker.domain.imports.exceptions import CatalogUnavailableError
from import_worker.shared.settings import Settings
from import_worker.worker.runner import build_use_case, run


class ScriptedUseCase:
    """Returns or raises the scripted outcomes, one per call."""

    def __init__(self, outcomes: list[ImportReport | Exception]) -> None:
        self.outcomes = outcomes
        self.calls = 0

    def execute(self) -> ImportReport:
        outcome = self.outcomes[self.calls]
        self.calls += 1
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def test_run_polls_and_sleeps_between_iterations() -> None:
    use_case = ScriptedUseCase([ImportReport(processed=1, failed=0)] * 3)
    sleeps: list[float] = []

    run(use_case, poll_interval_seconds=2.5, sleep=sleeps.append, max_iterations=3)

    assert use_case.calls == 3
    assert sleeps == [2.5, 2.5, 2.5]


def test_run_keeps_going_when_catalog_is_down(caplog: pytest.LogCaptureFixture) -> None:
    use_case = ScriptedUseCase(
        [CatalogUnavailableError(), ImportReport(processed=1, failed=0)]
    )

    run(use_case, poll_interval_seconds=0, sleep=lambda _: None, max_iterations=2)

    assert use_case.calls == 2
    assert "Catalog service is unavailable" in caplog.text


def test_build_use_case_creates_inbox_directories(tmp_path: Path) -> None:
    settings = Settings(
        inbox_dir=tmp_path / "inbox",
        processed_dir=tmp_path / "processed",
        failed_dir=tmp_path / "failed",
    )

    build_use_case(settings)

    assert (tmp_path / "inbox").is_dir()
