from os import getenv
from celery import Celery

REDIS = getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("xenyou", broker=REDIS, backend=REDIS)
celery_app.conf.task_routes = {"app.tasks.*": {"queue": "default"}}

celery_app.conf.beat_schedule = {
    "train-recommender-daily": {
        "task": "app.tasks.recommender.train_recommender",
        "schedule": 86400.0,  # every 24h
    },
}


celery_app.conf.timezone = "UTC"
