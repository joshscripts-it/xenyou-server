# app/routers/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from app.models.models import User, StudentProfile, LandlordProfile, AdminProfile
from app.schemas.schemas import UserCreate, Token, Login
from app.auth import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from starlette.concurrency import run_in_threadpool
from app.services.embeddings import EmbeddingService

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["auth"])
embedding_service = EmbeddingService()


@router.post("/signup")
async def signup(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user (student, landlord, or admin)."""

    # Check if user already registered
    stmt = select(User).where(User.email == payload.email)
    existing = await db.execute(stmt)
    if existing.scalars().first():
        raise HTTPException(400, "Email already exists")

    if payload.role not in ("student", "landlord", "admin"):
        raise HTTPException(400, "Invalid role")

    # create new user
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        phone=payload.phone,
        firstname=payload.firstname,
        lastname=payload.lastname,
    )

    db.add(user)
    await db.flush()  # Get user.id

    if payload.role == "student":
        # Generate embedding for student profile
        text_to_embed = f"{payload.firstname} {payload.lastname} {payload.email}"
        embedding = await run_in_threadpool(embedding_service.embed, text_to_embed)

        sp = StudentProfile(
            user_id=user.id,
            student_id=str(user.id),
            embedding_vector=embedding,
        )
        db.add(sp)
    elif payload.role == "landlord":
        lp = LandlordProfile(user_id=user.id)
        db.add(lp)
    else:
        ap = AdminProfile(user_id=user.id)
        db.add(ap)

    await db.commit()

    access = create_access_token(user.id)
    refresh = await create_refresh_token(user.id)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(payload: Login, db: AsyncSession = Depends(get_db)) -> Token:
    """Authenticate user and return access/refresh tokens."""

    stmt = select(User).where(User.email == payload.email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access = create_access_token(user.id)
    refresh = await create_refresh_token(user.id)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
