import pytest

from import_worker.domain.imports.batch import ItemBatch
from import_worker.domain.imports.exceptions import InvalidBatchError


def test_create_strips_names() -> None:
    batch = ItemBatch.create("a.json", ["  pen ", "book"])

    assert batch.names == ("pen", "book")
    assert batch.source == "a.json"


def test_create_rejects_empty_batch() -> None:
    with pytest.raises(InvalidBatchError, match=r"a\.json: no items"):
        ItemBatch.create("a.json", [])


@pytest.mark.parametrize("name", ["", "   ", "x" * 101])
def test_create_rejects_invalid_name(name: str) -> None:
    with pytest.raises(InvalidBatchError):
        ItemBatch.create("a.json", ["pen", name])
