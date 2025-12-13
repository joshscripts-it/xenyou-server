from app.celery_app import celery
from app.database import get_session
from app.services.recommender import RecommenderService


@celery.task(name="app.tasks.recommender.train_recommender")
def train_recommender():
    recommender = RecommenderService()
    with next(get_session()) as session:
        ok = recommender.train(session)
        return "✅ Training complete" if ok else "⚠️ No data to train yet"
