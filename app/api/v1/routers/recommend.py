from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.services.recommender import RecommenderService
from app.models.models import Property, User
from app.deps.dependencies import get_current_user
from app.tasks.recommender import train_recommender
from app.schemas.schemas import RecommendationRequest, RecommendationResponse

router = APIRouter()
recommender = RecommenderService()


@router.post("/train")
async def trigger_training():
    """Trigger background training task for the recommender."""
    task = train_recommender.delay()  # async call via Celery
    return {"task_id": task.id, "status": "queued"}


@router.post("/for-student", response_model=RecommendationResponse)
async def recommend_for_student(
    payload: RecommendationRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get property recommendations for a specific student."""

    # Only students may request recommendations
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail=f"Sorry you are a {current_user.role}. Only students may access recommendations",
        )

    property_ids = await recommender.recommend(str(payload.student_id), session)

    if not property_ids:
        return {"message": "No recommendations yet"}

    stmt = select(Property).where(Property.id.in_(property_ids))
    result = await session.execute(stmt)
    properties = result.scalars().all()
    filtered = [p for p in properties if p.id in property_ids]

    return {"recommendations": filtered}
