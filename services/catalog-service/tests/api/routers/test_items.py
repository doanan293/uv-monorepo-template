from uuid import uuid4

from fastapi.testclient import TestClient

from fakes import FakeItemRepository


def test_create_item_returns_201(client: TestClient) -> None:
    response = client.post("/api/v1/items", json={"name": "pen"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "pen"
    assert {"id", "name", "created_at"} == body.keys()


def test_get_item_after_create_returns_200(client: TestClient) -> None:
    created = client.post("/api/v1/items", json={"name": "pen"}).json()

    response = client.get(f"/api/v1/items/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_unknown_item_returns_404(client: TestClient) -> None:
    item_id = uuid4()

    response = client.get(f"/api/v1/items/{item_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Item {item_id} not found"}


def test_get_item_with_invalid_uuid_returns_422(client: TestClient) -> None:
    assert client.get("/api/v1/items/abc").status_code == 422


def test_create_item_with_blank_name_returns_422(
    client: TestClient, fake_repository: FakeItemRepository
) -> None:
    response = client.post("/api/v1/items", json={"name": "   "})

    assert response.status_code == 422
    assert fake_repository.items == {}


def test_create_item_without_name_returns_422(client: TestClient) -> None:
    assert client.post("/api/v1/items", json={}).status_code == 422


def test_openapi_documents_not_found(client: TestClient) -> None:
    responses = client.get("/openapi.json").json()["paths"]["/api/v1/items/{item_id}"][
        "get"
    ]["responses"]

    assert "404" in responses
