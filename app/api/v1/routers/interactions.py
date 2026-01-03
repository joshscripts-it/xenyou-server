# Interaction Logging Service → Track what students do (click, save, apply).
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import InteractionEvent, User
from app.schemas.schemas import InteractionRequest, InteractionResponse
from app.deps.dependencies import get_current_user

router = APIRouter()


@router.post("/log", response_model=InteractionResponse)
async def log_interaction(
    payload: InteractionRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Log a user interaction event (view, click, save, skip, etc.)."""

    interaction = InteractionEvent(
        user_id=current_user.id,
        property_id=payload.property_id,
        event_type=payload.event_type,
    )

    session.add(interaction)
    await session.commit()
    await session.refresh(interaction)

    return {
        "message": "✅ Interaction logged successfully",
        "interaction": {
            "user_id": interaction.user_id,
            "property_id": interaction.property_id,
            "event_type": interaction.event_type,
        },
    }
