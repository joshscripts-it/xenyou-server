# Interaction Logging Service → Track what students do (click, save, apply).
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import InteractionEvent

router = APIRouter()


@router.post("/log")
async def log_interaction(
    student_id: int,
    property_id: int,
    event_type: str,
    session: AsyncSession = Depends(get_db),
):
    """Log a user interaction event (view, click, save, skip, etc.)."""

    interaction = InteractionEvent(
        user_id=student_id, property_id=property_id, event_type=event_type
    )
    session.add(interaction)
    await session.commit()
    return {"message": "Interaction logged"}
