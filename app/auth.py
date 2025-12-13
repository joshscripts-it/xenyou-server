# app/auth.py
import os
from datetime import datetime, timedelta
import jwt
from app.db.session import async_session_maker
from app.models.models import RefreshToken
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID
from passlib.context import CryptContext

# from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = int(os.getenv("ACCESS_EXPIRE_MINUTES", "15"))
REFRESH_EXPIRE_DAYS = int(os.getenv("REFRESH_EXPIRE_DAYS", "30"))


pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"


def create_access_token(sub: UUID | str):
    now = datetime.utcnow()
    exp = now + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    payload = {
        "sub": str(sub),
        "iat": now.timestamp(),
        "exp": exp.timestamp(),
        "type": "access",
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def create_refresh_token(sub: UUID | str) -> str:
    """Create and persist a refresh token."""
    now = datetime.utcnow()
    exp = now + timedelta(days=REFRESH_EXPIRE_DAYS)
    payload = {
        "sub": str(sub),
        "iat": now.timestamp(),
        "exp": exp.timestamp(),
        "type": "refresh",
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Persist refresh token in database
    # Ensure user_id is a UUID instance
    try:
        user_id = sub if isinstance(sub, UUID) else UUID(str(sub))
    except Exception:
        user_id = sub

    async with async_session_maker() as db:
        rt = RefreshToken(user_id=user_id, token=token, created_at=now, expires_at=exp)
        db.add(rt)
        await db.commit()

    return token


def decode_token(token: str):
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hash):
    return pwd_context.verify(password, hash)
