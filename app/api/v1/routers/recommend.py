from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.services.recommender import RecommenderService
from app.models.models import Property
from app.tasks.recommender import train_recommender

router = APIRouter()
recommender = RecommenderService()


@router.post("/train")
async def trigger_training():
    """Trigger background training task for the recommender."""
    task = train_recommender.delay()  # async call via Celery
    return {"task_id": task.id, "status": "queued"}


@router.get("/for-student/{student_id}")
async def recommend_for_student(
    student_id: int, session: AsyncSession = Depends(get_db)
):
    """Get property recommendations for a specific student."""

    property_ids = recommender.recommend(student_id, session)

    if not property_ids:
        return {"message": "No recommendations yet"}

    stmt = select(Property).where(Property.id.in_(property_ids))
    result = await session.execute(stmt)
    properties = result.scalars().all()
    filtered = [p.dict() for p in properties if p.id in property_ids]

    return {"recommendations": filtered}
