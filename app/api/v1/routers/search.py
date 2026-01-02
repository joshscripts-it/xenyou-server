from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db.session import get_db
from app.models.models import Property, InteractionEvent, User
from app.deps.dependencies import get_current_user

from app.services.embeddings import EmbeddingService
from typing import Optional
from app.schemas.schemas import SearchRequest, SearchResponse
from sqlalchemy.orm import selectinload
from starlette.concurrency import run_in_threadpool

router = APIRouter()
embedding_service = EmbeddingService()


# Search endpoint (unchanged)
@router.post("/", response_model=SearchResponse)
async def search_hostels(
    payload: SearchRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Get properties with features that have embedding vectors
    from app.models.models import PropertyFeature

    h_stmt = select(Property).where(Property.is_available == True)
    if payload.max_price is not None:
        h_stmt = h_stmt.where(Property.price <= payload.max_price)
    h_stmt = h_stmt.options(selectinload(Property.features))

    result = await session.execute(h_stmt)
    hostels = result.scalars().all()
    query_emb = await run_in_threadpool(embedding_service.embed, payload.query)

    # use inner product (matches pgvector inner product semantics)
    def inner_product(v1, v2):
        import numpy as np

        v1, v2 = np.array(v1), np.array(v2)
        return float(np.dot(v1, v2))

    results = []
    for h in hostels:
        # Get embedding from PropertyFeature if available
        embedding = h.features.embedding_vector if h.features else None
        if not embedding:
            continue
        sim = inner_product(query_emb, embedding)
        results.append(
            {
                "id": str(h.id),
                "title": h.title,
                "description": h.description,
                "price": h.price,
                "score": sim,
            }
        )

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"results": sorted_results}


# 👇 NEW: listing detail with auto logging
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
