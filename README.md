# uv-monorepo-template

Python monorepo template for AI-assisted development (AIDD). Humans and coding agents
share one set of rules (`AGENTS.md`, `docs/engineering-guide.md`,
`.github/CONTRIBUTING.md`), and the tooling enforces them.

- **uv workspace** — every service under `services/` is an independent package; one
  `uv.lock` and one `.venv` at the root.
- **Clean Architecture** — `api|worker → application → domain ← infra`; see
  [`docs/engineering-guide.md`](docs/engineering-guide.md).
- **Tooling** — ruff (lint + format), pyrefly (types), pytest (coverage ≥ 80%),
  gitleaks (secrets), hadolint (Dockerfiles), all wired into pre-commit and CI.
- **Samples** — three small services that work together:

| Service | Kind | What it shows |
|---|---|---|
| [`catalog-service`](services/catalog-service) | HTTP API | The basic layers: CRUD on `items` |
| [`order-service`](services/order-service) | HTTP API | Calling another service through a port + HTTP adapter |
| [`import-worker`](services/import-worker) | Background worker | A non-HTTP entry point; file and HTTP adapters |

```
import-worker ──POST /api/v1/items──► catalog-service ◄──GET /api/v1/items/{id}── order-service
```

Services never import each other's code; they talk over HTTP.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) 0.12.13 (installs Python 3.12 for you)
- Docker with Compose v2 (for `docker compose` and the hadolint hook)

## Quickstart

```bash
uv sync                          # create .venv with every service and dev tool
uv run pre-commit install        # run the hooks on every commit
cp .env.example .env             # local settings; never commit .env

# Run services from the repository root: settings read ./.env from the
# current directory, and the root .env is the only one. One terminal each:
uv run catalog-service           # http://localhost:8000/docs
uv run order-service             # http://localhost:8001/docs
uv run import-worker             # polls data/inbox/

# Or the whole stack in containers:
docker compose up --build
```

Try it:

```bash
# Import items through the worker
echo '{"items": [{"name": "pen"}]}' > data/inbox/items.json         # local run
docker compose cp data/inbox/items.json import-worker:/app/data/inbox/  # compose

# Order an existing item
ITEM_ID=$(curl -s -X POST localhost:8000/api/v1/items \
  -H 'content-type: application/json' -d '{"name": "cup"}' | python3 -c 'import sys, json; print(json.load(sys.stdin)["id"])')
curl -X POST localhost:8001/api/v1/orders -H 'content-type: application/json' \
  -d "{\"item_id\": \"$ITEM_ID\", \"quantity\": 2}"
```

## Layout

```
.
├── AGENTS.md                 # rules for coding agents
├── CLAUDE.md                 # imports AGENTS.md (@AGENTS.md) for Claude Code
├── docs/                     # engineering guide (architecture + code rules), prompting guide
├── services/
│   ├── catalog-service/      # sample HTTP API: src/, tests/, pyproject.toml
│   ├── order-service/        # sample HTTP API that calls catalog-service
│   └── import-worker/        # sample background worker
├── devops/Dockerfile         # one image recipe for every service (build arg SERVICE)
├── docker-compose.yml        # local stack
├── pyproject.toml            # workspace root + pinned dev tools
├── ruff.toml                 # the only Ruff configuration
├── .pre-commit-config.yaml
├── .github/                  # CI, CONTRIBUTING.md, issue and PR templates
└── .env.example              # every environment variable, documented
```

## Start your project from this template

The three services are samples. The rules in `AGENTS.md`, `docs/` and `.github/`
do not mention them, so they keep working after you delete them.

1. Rewrite this README's title and introduction for your project.
2. Add your first service (below), using a sample as the starting point.
3. Delete the samples you no longer need: their directory under `services/`, their
   block in `docker-compose.yml` and their section in `.env.example`.
4. `uv sync`, then run the checks.

## Add a new service

Names: directory and package `<name>` use dashes (`billing-service`); the Python
package uses underscores (`billing_service`); the environment prefix is
`BILLING_SERVICE_`.

1. Copy the closest sample without caches — an API: `catalog-service`; an API that
   calls another service: `order-service`; a worker: `import-worker`:
   `rsync -a --exclude '.*cache' --exclude '.coverage' services/catalog-service/ services/<name>/`.
2. Rename `src/catalog_service` to `src/<name_with_underscores>`, and replace
   `catalog-service` / `catalog_service` / `CATALOG_SERVICE_` with the new names in
   `pyproject.toml`, `README.md`, source and tests. The environment prefix must be
   unique per service, because all services read the same root `.env`.
3. Replace the sample feature with your own; keep the layer layout.
4. Add its variables to `.env.example` and a service entry to `docker-compose.yml`
   (build arg `SERVICE: <name>`).
5. `uv sync` from the root.

CI, pre-commit and `devops/Dockerfile` discover services by directory, so they need
no change.

## Checks

```bash
# inside a service directory
uv run ruff check . && uv run ruff format --check .
uv run pyrefly check --min-severity warn
uv run pytest --cov=src --cov-fail-under=80

# from the repository root
uv run pre-commit run --all-files
```

CI runs three jobs on every pull request: `lint` (ruff, pyrefly), `test` (services
with changes) and `secret-scan` (gitleaks).

## Documentation

| File | Contents |
|---|---|
| [`docs/engineering-guide.md`](docs/engineering-guide.md) | Architecture, layer rules, code style, testing, API, Docker Compose |
| [`docs/prompting-instruction.md`](docs/prompting-instruction.md) | How to write LLM prompts |
| [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) | Branches, commits, CI, pull requests, reviewing and merging |
| [`.github/ISSUE_TEMPLATE/task.md`](.github/ISSUE_TEMPLATE/task.md) | Issue template (shown by GitHub on "New issue") |
| [`.github/pull_request_template.md`](.github/pull_request_template.md) | Pull request template |

## License

[MIT No Attribution](LICENSE) — use, modify, distribute and sell it for any purpose,
with no need to keep the copyright notice.
