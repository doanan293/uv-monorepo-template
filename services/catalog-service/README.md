# catalog-service

Sample FastAPI service that shows the basic Clean Architecture layout of this template.
`order-service` and `import-worker` call its API.
Copy it to start a new service (see the root `README.md`, "Add a new service").

## Endpoints

| Method | Path | Success | Errors |
|---|---|---|---|
| `GET` | `/health` | `200 {"status": "ok"}` | |
| `POST` | `/api/v1/items` | `201` new item | `422` blank, missing or > 100-character name |
| `GET` | `/api/v1/items/{item_id}` | `200` item | `404` unknown id, `422` id is not a UUID |

```bash
curl -X POST localhost:8000/api/v1/items -H 'content-type: application/json' -d '{"name": "pen"}'
# {"id": "1b0ce4ef-...", "name": "pen", "created_at": "2026-11-09T10:44:23Z"}
```

Interactive docs: `http://localhost:8000/docs`.

## Layers

| Path | Layer | Contents |
|---|---|---|
| `src/catalog_service/domain/items/` | domain | `Item` entity, `ItemRepository` port, domain errors |
| `src/catalog_service/application/items/` | application | `CreateItem`, `GetItem` use cases |
| `src/catalog_service/infra/memory/` | infra | `InMemoryItemRepository` adapter |
| `src/catalog_service/api/` | api | routers, schemas, `dependencies.py` (composition root) |
| `src/catalog_service/shared/` | shared | settings, base exceptions |
| `src/catalog_service/main.py` | entry point | runs uvicorn |

`InMemoryItemRepository` loses data on restart; replace it with a database adapter that
implements `ItemRepository`, and change only `api/dependencies.py`.

## Run and test

Serve from the repository root, so the root `.env` is loaded:

```bash
uv run catalog-service                      # serve on CATALOG_SERVICE_HOST:CATALOG_SERVICE_PORT
```

Test and check from this directory:

```bash
uv run pytest --cov=src --cov-fail-under=80
uv run ruff check . && uv run ruff format --check .
uv run pyrefly check --min-severity warn
```
