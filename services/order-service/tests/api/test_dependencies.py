from order_service.api.dependencies import get_item_catalog, get_order_repository


def test_default_dependencies_are_singletons() -> None:
    assert get_order_repository() is get_order_repository()
    assert get_item_catalog() is get_item_catalog()
