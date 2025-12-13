from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.db.session import get_db
from app.models.models import Property
from app.services.embeddings import EmbeddingService

router = APIRouter()
embedding_service = EmbeddingService()


@router.post("/add")
async def add_property(
    title: str,
    description: str,
    price: int,
    location: str = "",
    session: AsyncSession = Depends(get_db),
):
    """Add a new property listing."""

    # Generate embedding for the property description
    emb = embedding_service.embed(description)

    property_obj = Property(
        id=uuid4(),
        title=title,
        description=description,
        price=price,
        location_text=location,
        embedding_vector=emb,
    )

    session.add(property_obj)
    await session.commit()
    await session.refresh(property_obj)

    return {"message": "Property added", "id": str(property_obj.id)}
