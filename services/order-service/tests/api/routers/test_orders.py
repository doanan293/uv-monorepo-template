from uuid import uuid4

from fastapi.testclient import TestClient

from fakes import FakeItemCatalog, FakeOrderRepository


def test_place_order_returns_201(
    client: TestClient, fake_catalog: FakeItemCatalog
) -> None:
    item_id = uuid4()
    fake_catalog.item_ids.add(item_id)

    response = client.post(
        "/api/v1/orders", json={"item_id": str(item_id), "quantity": 2}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["item_id"] == str(item_id)
    assert body["quantity"] == 2
    assert {"id", "item_id", "quantity", "created_at"} == body.keys()


def test_get_order_after_place_returns_200(
    client: TestClient, fake_catalog: FakeItemCatalog
) -> None:
    item_id = uuid4()
    fake_catalog.item_ids.add(item_id)
    created = client.post(
        "/api/v1/orders", json={"item_id": str(item_id), "quantity": 1}
    ).json()

    response = client.get(f"/api/v1/orders/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_place_order_for_unknown_item_returns_422(
    client: TestClient, fake_orders: FakeOrderRepository
) -> None:
    item_id = uuid4()

    response = client.post(
        "/api/v1/orders", json={"item_id": str(item_id), "quantity": 1}
    )

    assert response.status_code == 422
    assert response.json() == {"detail": f"Item {item_id} is not in the catalog"}
    assert fake_orders.orders == {}


def test_place_order_with_bad_quantity_returns_422(client: TestClient) -> None:
    response = client.post(
        "/api/v1/orders", json={"item_id": str(uuid4()), "quantity": 0}
    )

    assert response.status_code == 422


def test_place_order_when_catalog_down_returns_503(
    client: TestClient, fake_catalog: FakeItemCatalog
) -> None:
    fake_catalog.is_available = False

    response = client.post(
        "/api/v1/orders", json={"item_id": str(uuid4()), "quantity": 1}
    )

    assert response.status_code == 503
    assert response.json() == {"detail": "Catalog service is unavailable"}


def test_get_unknown_order_returns_404(client: TestClient) -> None:
    order_id = uuid4()

    response = client.get(f"/api/v1/orders/{order_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Order {order_id} not found"}


def test_get_order_with_invalid_uuid_returns_422(client: TestClient) -> None:
    assert client.get("/api/v1/orders/abc").status_code == 422


def test_openapi_documents_error_statuses(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]

    assert "503" in paths["/api/v1/orders"]["post"]["responses"]
    assert "404" in paths["/api/v1/orders/{order_id}"]["get"]["responses"]
