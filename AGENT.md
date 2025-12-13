# Agent Notes for XenYou

Purpose
- Short, actionable notes for an automated agent making code changes in this repository.

Quick rules
- Always inspect `app/main.py` and the router being changed before editing handlers.
- Use dependency injection (see `app/deps/dependencies.py`) for DB/auth resources; do not create global DB sessions.
- Keep DB operations in `crud/` and business logic in `app/services/`.
- Long-running jobs must be Celery tasks in `app/tasks/` and registered in `app/celery_app.py`.

Local dev commands
- Activate virtualenv and install deps:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
- Run tests:
```bash
pytest -q
```

When changing models
- Update SQLAlchemy models in `app/models/`.
- Add or update `crud/*` helpers as needed.
- Generate an Alembic migration and include it in PRs: `alembic revision --autogenerate -m "..."`.

What to include in PRs
- List of modified files and brief rationale.
- If DB schema changed: include Alembic migration.
- If new background tasks added: document how to start Celery and any env vars.

If uncertain
- Ask the repo owner which external services (broker, vector DB, model endpoints) are available in the test environment.
