from catalog_service.api.dependencies import get_item_repository


def test_default_repository_is_singleton() -> None:
    assert get_item_repository() is get_item_repository()
