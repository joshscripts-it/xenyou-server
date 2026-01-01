# Interaction Logging Service → Track what students do (click, save, apply).
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import InteractionEvent

router = APIRouter()


@router.post("/log")
async def log_interaction(
    user_id: str,
    property_id: str,
    event_type: str,
    session: AsyncSession = Depends(get_db),
):
    """Log a user interaction event (view, click, save, skip, etc.)."""

    interaction = InteractionEvent(
        user_id=user_id, property_id=property_id, event_type=event_type
    )
    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)

    return {
        "message": "✅ Interaction logged successfully",
        "interaction": {
            "user_id": str(interaction.user_id),
            "property_id": str(interaction.property_id),
            "event_type": interaction.event_type,
        },
    }
