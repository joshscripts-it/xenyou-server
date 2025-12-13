from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db.session import get_db
from app.models.models import Property
from app.services.embeddings import EmbeddingService
from pydantic import BaseModel

router = APIRouter()
embedding_service = EmbeddingService()


class Query(BaseModel):
    text: str
    max_price: int | None = None


@router.post("/search")
async def search(query: Query, session: AsyncSession = Depends(get_db)):
    """Search for properties based on query text and optional price filter."""

    # 1. Embed the query
    q_emb = embedding_service.embed(query.text)

    # 2. Search with pgvector (cosine distance)
    statement = select(Property).order_by(Property.embedding_vector).limit(5)
    result = await session.execute(statement)
    properties = result.scalars().all()

    # 3. Apply price filter
    if query.max_price:
        properties = [p for p in properties if p.price and p.price <= query.max_price]

    return {"results": [p.dict() for p in properties]}
