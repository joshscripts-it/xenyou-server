<!-- .github/copilot-instructions.md: Project-specific instructions for AI coding agents -->
# Copilot / Agent Instructions for XenYou

This file gives focused, actionable knowledge to help an AI coding agent be productive in this repository.

Summary
- This project is a FastAPI-based backend (see `app/main.py`) with SQLAlchemy DB layers, Pydantic schemas, Celery background tasks, and a recommender/embedding service.

Key components (what to read first)
- `app/main.py`: application entrypoint and router mounting.
- `app/routers/`: FastAPI route handlers (auth, users, search, recommend, hostels, interactions).
- `app/models/` and `app/schemas/`: SQLAlchemy models and Pydantic schemas — use these to understand data shape.
- `crud/`: database CRUD helpers (e.g. `crud/user.py`) — use for standard DB operations.
- `app/db/session.py` and `db/init.sql`: DB session management and initial SQL — follow existing patterns for DB access.
- `alembic/`: migrations; do not modify DB schema without updating `alembic`.
- `app/celery_app.py` and `app/tasks/`: Celery configuration and background tasks (recommender training, etc.).
- `app/services/`: contains `embeddings.py`, `recommender.py`, `scheduler.py` — core ML/recommendation logic.

Project-specific patterns & conventions
- Dependency Injection: use FastAPI `Depends(...)` where present; inspect `app/deps/dependencies.py` for common DI helpers (e.g., auth, paginated parameters, current user patterns).
- DB lifetime: follow `app/db/session.py` for obtaining a `Session` via dependency injection (don't create ad-hoc global sessions). Use the provided `get_db`/context patterns.
- CRUD vs. Models vs. Schemas: write DB logic in `crud/*`, keep business logic in `services/*`, use Pydantic schemas in `schemas/*` for validation and serialization.
- Async vs sync: handlers in `app/routers` are standard FastAPI handlers — match the existing style (if route is defined sync, keep sync; if async, keep async). Check each router for precedence.
- Background work: heavy or long-running tasks should be moved to Celery tasks in `app/tasks/` and invoked via `app/celery_app.py` (not as blocking calls in request handlers).

Testing & developer workflows
- Virtualenv: the repository commonly uses a local `.venv`. Typical setup:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- Run tests with `pytest` from repo root. Example: `pytest -q tests/test_users.py`.
- Migrations: use Alembic in `alembic/` to manage schema changes. If you change models, run `alembic revision --autogenerate -m "msg"` and apply with `alembic upgrade head`.
- Celery: to run worker use the app's Celery config. Inspect `app/celery_app.py` before launching workers; run with something like `celery -A app.celery_app.worker worker --loglevel=info` (adjust for local settings/environment variables).

Integration points & external dependencies
- Embeddings & recommender: `app/services/embeddings.py` and `app/services/recommender.py` — these may call external ML services or local models. Look at those files to discover API keys or endpoints.
- External stores: check `config.py` and `app/core/config.py` for settings (DB URL, external API endpoints, credentials). Prefer reading environment variables used there.
- Message queue & worker: Celery requires a broker (Redis/RabbitMQ) and result backend configured via environment/config.

What an agent should do first when modifying code
- Read `app/main.py`, then the specific `router` handler affected (e.g., `app/routers/users.py`) and the corresponding `crud` and `schema` files.
- For DB changes: update `models/*`, `crud/*` if needed, and create an Alembic migration.
- For background work: implement or update tasks in `app/tasks/` and invoke via `app/celery_app.py`.

Examples (small pointers)
- To add a new user route: create route in `app/routers/users.py`, call `crud/user.py` functions, accept/return Pydantic models from `app/schemas/user.py`.
- To add a recommender job: add logic to `app/services/recommender.py`, expose a Celery task in `app/tasks/recommender.py`, and schedule/invoke from the router or `scheduler.py`.

Files to reference in PR reviews
- `app/main.py`, changed `routers/*`, `crud/*`, `app/models/*`, `app/schemas/*`, `app/services/*`, `app/tasks/*`, and `alembic/` revisions.

Limitations
- This file documents only repository-discoverable patterns. If behavior depends on external infra (broker, vector DB, cloud keys), confirm the runtime environment and secrets.

If anything below is unclear or you'd like more examples from specific files, ask and I'll expand with concrete code snippets from the repository.
