from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db.session import get_db
from app.models.models import Property, InteractionEvent

from app.services.embeddings import EmbeddingService
from typing import Optional

router = APIRouter()
embedding_service = EmbeddingService()


# Search endpoint (unchanged)
@router.post("/")
async def search_hostels(
    query: str, max_price: Optional[int] = None, session: AsyncSession = Depends(get_db)
):

    # Get properties with features that have embedding vectors
    from app.models.models import PropertyFeature

    h_stmt = select(Property).where(Property.is_available == True)

    result = await session.execute(h_stmt)
    hostels = result.scalars().all()
    query_emb = embedding_service.embed(query)

    # naive similarity (dot product or cosine similarity)
    def cosine_sim(v1, v2):
        import numpy as np

        v1, v2 = np.array(v1), np.array(v2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    results = []
    for h in hostels:
        if max_price and h.price and h.price > max_price:
            continue
        # Get embedding from PropertyFeature if available
        embedding = h.features.embedding_vector if h.features else None
        if not embedding:
            continue
        sim = cosine_sim(query_emb, embedding)
        results.append(
            {
                "id": str(h.id),
                "title": h.title,
                "description": h.description,
                "price": h.price,
                "score": sim,
            }
        )

    return sorted(results, key=lambda x: x["score"], reverse=True)


# 👇 NEW: Hostel detail with auto logging
@router.get("/hostel/{hostel_id}")
async def get_hostel_detail(
    hostel_id: str,
    user_id: str,
    session: AsyncSession = Depends(get_db),
):
    hostel_stmt = select(Property).where(Property.id == hostel_id)
    result = await session.execute(hostel_stmt)
    hostel = result.scalars().first()

    if not hostel:
        return {"error": "Property not found"}

    # ✅ Auto-log viewed interaction
    interaction = InteractionEvent(
        user_id=user_id, property_id=hostel_id, event_type="viewed"
    )
    session.add(interaction)
    await session.commit()

    return {
        "message": "✅ Property fetched + view logged",
        "property": {
            "id": str(hostel.id),
            "title": hostel.title,
            "description": hostel.description,
            "price": hostel.price,
        },
    }
