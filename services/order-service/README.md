# order-service

Sample FastAPI service that places orders for items held by `catalog-service`. It shows
how one service calls another without sharing code: a port in `domain`, an HTTP
adapter in `infra`.

## Endpoints

| Method | Path | Success | Errors |
|---|---|---|---|
| `GET` | `/health` | `200 {"status": "ok"}` | |
| `POST` | `/api/v1/orders` | `201` new order | `422` quantity not 1-1000, item not in the catalog, bad body; `503` catalog unavailable |
| `GET` | `/api/v1/orders/{order_id}` | `200` order | `404` unknown id, `422` id is not a UUID |

```bash
curl -X POST localhost:8001/api/v1/orders -H 'content-type: application/json' \
  -d '{"item_id": "1b0ce4ef-3055-4f49-8743-fb19833a6dc1", "quantity": 2}'
# {"id": "...", "item_id": "1b0ce4ef-...", "quantity": 2, "created_at": "..."}
```

Interactive docs: `http://localhost:8001/docs`.

## Layers

| Path | Layer | Contents |
|---|---|---|
| `src/order_service/domain/orders/` | domain | `Order` entity, `OrderRepository` and `ItemCatalog` ports, domain errors |
| `src/order_service/application/orders/` | application | `PlaceOrder`, `GetOrder` use cases |
| `src/order_service/infra/memory/` | infra | `InMemoryOrderRepository` adapter |
| `src/order_service/infra/catalog_http/` | infra | `HttpItemCatalog`: asks catalog-service over HTTP |
| `src/order_service/api/` | api | routers, schemas, `dependencies.py` (composition root) |
| `src/order_service/shared/` | shared | settings, base exceptions |

`PlaceOrder` validates the quantity first, so a bad request never reaches the catalog.

## Run and test

Serve from the repository root (needs `catalog-service` on `ORDER_SERVICE_CATALOG_URL`):

```bash
uv run order-service                        # serve on ORDER_SERVICE_HOST:ORDER_SERVICE_PORT
```

Test and check from this directory:

```bash
uv run pytest --cov=src --cov-fail-under=80
uv run ruff check . && uv run ruff format --check .
uv run pyrefly check --min-severity warn
```
