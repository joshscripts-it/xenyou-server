from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4
from app.db.session import get_db
from app.models.models import Property, User, LandlordProfile
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.schemas.schemas import PropertyCreate
from app.services.embeddings import EmbeddingService
from app.deps.dependencies import get_current_user


router = APIRouter()
embedding_service = EmbeddingService()


@router.post("/add")
async def add_property(
    payload: PropertyCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a new property listing."""
    # print(f"CURRENT USER ID: {current_user.id}")

    # Only landlords or admins may add properties
    if current_user.role not in ("landlord", "admin"):
        raise HTTPException(
            status_code=403, detail="Only landlords or admins may add properties"
        )

    # Determine landlord_id: landlords use their own profile, admins must provide one
    if current_user.role == "landlord":
        stmt = select(LandlordProfile).where(LandlordProfile.user_id == current_user.id)
        res = await session.execute(stmt)
        lp = res.scalars().first()
        if not lp:
            raise HTTPException(
                status_code=400, detail="Landlord profile not found for current user"
            )
        landlord_id = lp.id
    else:
        # admin
        landlord_id = payload.landlord_id

    # Ensure title is unique
    stmt = select(Property).where(Property.title == payload.title)
    res = await session.execute(stmt)
    if res.scalars().first():
        raise HTTPException(status_code=400, detail="Property title already exists")

    # Generate embedding for the property description
    emb = embedding_service.embed(payload.description)

    property_obj = Property(
        id=uuid4(),
        title=payload.title,
        landlord_id=landlord_id,
        type=payload.type,
        description=payload.description,
        price=payload.price,
        location_text=payload.location_text,
        embedding_vector=emb,
    )

    session.add(property_obj)
    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail="Integrity error while adding property"
        ) from err
    await session.refresh(property_obj)

    return {"message": "Property added", "id": str(property_obj.id)}
