from os import getenv
from celery import Celery

REDIS = getenv("REDIS_URL", "redis://localhost:6379/0")

# Try Redis; fall back to in-memory broker for local dev/testing
try:
    import redis
    redis.from_url(REDIS).ping()  # Test connection
    broker_url = REDIS
    backend_url = REDIS
except Exception:
    # Redis unavailable; use in-memory broker for local testing
    broker_url = "memory://"
    backend_url = "cache+memory://"

celery_app = Celery("xenyou", broker=broker_url, backend=backend_url)
celery_app.conf.task_routes = {"app.tasks.*": {"queue": "default"}}

celery_app.conf.beat_schedule = {
    "train-recommender-daily": {
        "task": "app.tasks.recommender.train_recommender",
        "schedule": 86400.0,  # every 24h
    },
}


celery_app.conf.timezone = "UTC"

# Backwards-compatible alias for callers expecting `celery`
celery = celery_app

__all__ = ["celery_app", "celery"]
