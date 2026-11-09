# import-worker

Sample background worker. Every few seconds it scans an inbox directory for `*.json`
files, creates each listed item in `catalog-service`, then moves the file to
`processed/` (or `failed/` when it cannot be imported). It shows a non-HTTP entry
layer (`worker/`) and two adapters: file system and HTTP.

## Import file format

```json
{"items": [{"name": "pen"}, {"name": "book"}]}
```

| Outcome | File moves to |
|---|---|
| Every item created | `processed/` |
| Not JSON, wrong shape, no items, a blank or > 100-character name, or the catalog rejects an item | `failed/` (reason in the log) |
| Catalog unavailable | stays in the inbox; retried on the next pass |

A retried file creates its items again, so a file interrupted halfway may produce
duplicates.

## Layers

| Path | Layer | Contents |
|---|---|---|
| `src/import_worker/domain/imports/` | domain | `ItemBatch`, `Inbox` and `ItemCatalog` ports, domain errors |
| `src/import_worker/application/imports/` | application | `ImportPendingFiles` use case |
| `src/import_worker/infra/filesystem/` | infra | `FileInbox`: inbox, processed and failed directories |
| `src/import_worker/infra/catalog_http/` | infra | `HttpItemCatalog`: creates items over HTTP |
| `src/import_worker/worker/` | worker | `runner.py`: composition root and polling loop |
| `src/import_worker/shared/` | shared | settings, base exceptions |

## Run and test

Run from the repository root (needs `catalog-service` on `IMPORT_WORKER_CATALOG_URL`):

```bash
uv run import-worker                        # polls IMPORT_WORKER_INBOX_DIR (data/inbox)
echo '{"items": [{"name": "pen"}]}' > data/inbox/items.json
```

With docker compose the inbox is the `import-data` volume:

```bash
docker compose cp items.json import-worker:/app/data/inbox/
```

Test and check from this directory:

```bash
uv run pytest --cov=src --cov-fail-under=80
uv run ruff check . && uv run ruff format --check .
uv run pyrefly check --min-severity warn
```
