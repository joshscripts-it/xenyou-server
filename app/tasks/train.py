from app.celery_app import celery_app
from app.db.session import get_db
from sqlmodel import select
from app.models.models import Interaction, Student, Hostel


@celery_app.task
def train_recommender():
    """
    Placeholder training task:
    - Load interactions and hostels
    - Train/update a recommender (stub for LightFM or other)
    """
    # Implement actual training here (LightFM / implicit / custom)
    # For now just log counts
    from app.db.session import create_session

    db = create_session()
    try:
        interactions = db.exec(select(Interaction)).all()
        hostels = db.exec(select(Hostel)).all()
        print(
            f"Training stub: {len(interactions)} interactions, {len(hostels)} hostels"
        )
    finally:
        db.close()
