# Engineering Guide

Rules for every service. Names like `Entity`, `<subdomain>` and `<other-service>` are
placeholders; the sample services follow these rules but nothing here depends on them.

## Layers

Clean Architecture (ports and adapters): dependencies point inward, toward `domain`.

```
api | worker ──► application ──► domain ◄── infra        shared ◄── every layer
```

```
services/<service-name>/
├── pyproject.toml        # dependencies, scripts, ruff/pytest/pyrefly config
├── src/<service_name>/
│   ├── api/              # HTTP entry layer (FastAPI) — or worker/ for a background worker
│   ├── application/<feature>/
│   ├── domain/<subdomain>/
│   ├── infra/<adapter>/
│   ├── shared/
│   └── main.py           # starts the server or the worker loop
└── tests/                # mirrors src/<service_name>/; test doubles in tests/fakes.py
```

| Layer | Contains | May import |
|---|---|---|
| `domain` | Entities, business rules, ports (`Protocol`), domain errors | `shared`, stdlib, pure libraries (`pydantic`) |
| `application` | Use cases that orchestrate `domain` through ports | `domain`, `shared` |
| `infra` | Adapters implementing ports: DB, HTTP, files, LLM | `domain`, `shared`, drivers, SDKs |
| `api` | Routers, request/response schemas, error → HTTP mapping | `application`, `shared`; `infra` only in `api/dependencies.py` |
| `worker` | Run loop and scheduling | `application`, `shared`; `infra` only in `worker/runner.py` |
| `shared` | Settings, base exceptions, constants | nothing from other layers |

## Rules

- **Composition root**: `api/dependencies.py` (or `worker/runner.py`) is the only place
  that builds `infra` adapters; use cases receive ports through their constructor
- `domain` does no I/O (network, DB, disk, processes); `infra` holds no business rules
- **Errors**: domain errors subclass `shared.exceptions` (`NotFoundError`,
  `InvalidInputError`, `ServiceUnavailableError`); `api/app.py` maps the base classes
  to `404` / `422` / `503`
- **Same layer**: modules in one layer do not import each other's services
  (`application/<A>` ↛ `application/<B>`, `infra/<A>` ↛ `infra/<B>`); share rules via
  `domain`, cross-layer helpers via `shared`
- **Between services**: never import another service's package; call it over HTTP
  through a port in your `domain` and an adapter in your `infra`
  (`infra/<other_service>_http/`). The port declares only the operations you need.
  The adapter turns transport errors and unexpected statuses into a
  `ServiceUnavailableError` subclass. The base URL comes from settings
  (`<SERVICE_NAME>_<OTHER_SERVICE>_URL`)

```python
# domain/<subdomain>/repository.py — port
class EntityRepository(Protocol):
    def get(self, entity_id: UUID) -> Entity | None: ...


# application/<feature>/get_entity.py — use case depends on the port
class GetEntity:
    def __init__(self, repository: EntityRepository) -> None: ...
    def execute(self, entity_id: UUID) -> Entity: ...  # raises EntityNotFoundError


# api/dependencies.py — composition root builds the adapter
@lru_cache
def get_entity_repository() -> InMemoryEntityRepository:
    return InMemoryEntityRepository()


# api/routers/entities.py — route maps the result to a response schema
@router.get("/{entity_id}")
def get_entity(
    entity_id: UUID, use_case: Annotated[GetEntity, Depends(get_get_entity)]
) -> EntityResponse:
    return EntityResponse.model_validate(use_case.execute(entity_id))
```

## Code

- Python 3.12, type hints on every signature, Google-style docstrings on public
  functions, methods and classes (tests exempt)
- Naming (PEP 8): classes are nouns (`PaymentProcessor`); functions are verbs
  (`send_email`); booleans start with `is_`/`has_`/`can_`; `@property` is a noun;
  modules are nouns (`user_service.py`), entry-point scripts are verbs (`run_server.py`)
- Functions: aim for 15–20 lines; ruff enforces complexity ≤ 10 (`C901`) and
  ≤ 40 statements (`PLR0915`)

## Tests

- Coverage ≥ 80% per service; unit tests for all `domain` and `application` logic
- Replace ports with fakes from `tests/fakes.py` instead of mocking libraries; no real
  database or network. HTTP adapters are tested with `httpx2.MockTransport`; API
  routes with `TestClient` and `app.dependency_overrides`
- Names: `test_*.py` files, `test_<behavior>` functions; set settings in tests with
  `monkeypatch.setenv`

## API

- REST + JSON under `/api/v1/` (except `/health`)
- Status codes: `201` created, `404` not found, `422` invalid input, `503` a dependency
  is down; business errors return `{"detail": "<message>"}`
- Document each endpoint with a route docstring, a request-schema example and its
  error statuses in `responses=` (published at `/docs`)

## Configuration and Docker

- Settings use `pydantic-settings` with a unique prefix per service
  (`<SERVICE_NAME>_`); every variable is documented in `.env.example`
- Every service builds from `devops/Dockerfile` with build arg
  `SERVICE=<service-name>` (directory = package = console-script name)
- In `docker-compose.yml`, reuse the `*service-defaults` and `*http-healthcheck`
  anchors; HTTP services listen on `8000` inside the container; services reach each
  other by service name (`http://<other-service>:8000`)
