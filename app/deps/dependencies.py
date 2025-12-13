from uuid import UUID as UUID_TYPE
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.auth import decode_token
from app.models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
) -> User:
    """
    Decode token and return User instance.
    Expects `sub` in token payload to be a UUID string.
    """
    payload = decode_token(token)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token (missing sub)")

    try:
        user_id = UUID_TYPE(str(sub))
    except Exception:
        raise HTTPException(
            status_code=401, detail="Invalid token subject; expected UUID"
        )

    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(role: str):
    async def inner(user: User = Depends(get_current_user)):
        if not getattr(user, "role", None):
            raise HTTPException(status_code=403, detail="User role not assigned")
        if user.role != role:
            raise HTTPException(status_code=403, detail=f"{role} role required")
        return user

    return inner
