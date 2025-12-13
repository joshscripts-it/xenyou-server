from typing import Optional
from uuid import UUID
import hashlib

from sqlmodel import select, Session

from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserUpdate


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(db: Session, user: UserCreate) -> Optional[UserModel]:
    exists = db.exec(
        select(UserModel).where(UserModel.username == user.username)
    ).first()
    if exists:
        return None
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=_hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: UUID) -> Optional[UserModel]:
    # db.get works with primary key types including UUID
    return db.get(UserModel, user_id)


def update_user(db: Session, user_id: UUID, user: UserUpdate) -> Optional[UserModel]:
    db_user = db.get(UserModel, user_id)
    if not db_user:
        return None
    if user.username is not None:
        db_user.username = user.username
    if user.email is not None:
        db_user.email = user.email
    if user.password is not None:
        db_user.hashed_password = _hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID) -> bool:
    db_user = db.get(UserModel, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
