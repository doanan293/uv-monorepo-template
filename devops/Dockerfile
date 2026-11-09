# syntax=docker/dockerfile:1
# Shared image for every service under services/. Build from the repository root:
#   docker build -f devops/Dockerfile --build-arg SERVICE=catalog-service .
# SERVICE is the directory under services/, which is also the package name and the
# console script name (services/catalog-service -> `catalog-service`).

FROM python:3.12-slim-bookworm AS build
COPY --from=ghcr.io/astral-sh/uv:0.12.13 /uv /bin/uv
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG SERVICE
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/app/.venv
WORKDIR /src
COPY pyproject.toml uv.lock ./
COPY services/ services/
RUN --mount=type=cache,target=/root/.cache/uv \
    test -n "${SERVICE}" \
    && uv sync --locked --no-dev --no-editable --package "${SERVICE}"

FROM python:3.12-slim-bookworm
ARG SERVICE
# Numeric IDs, so a runtime that enforces a non-root user can verify it.
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app --no-create-home app
WORKDIR /app
# Writable directory for services that keep files (e.g. import-worker's inbox).
RUN mkdir /app/data && chown 10001:10001 /app/data
COPY --from=build --chown=10001:10001 /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    SERVICE=${SERVICE}
USER 10001:10001
EXPOSE 8000
CMD ["sh", "-c", "exec \"$SERVICE\""]
