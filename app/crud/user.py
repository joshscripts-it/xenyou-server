from typing import Optional

# from uuid import UUID
import hashlib
from sqlmodel import select, Session

from app.models.models import User
from app.schemas.schemas import UserCreate
from app.auth import hash_password


# def _hash_password(password: str) -> str:
#     return hashlib.sha256(password.encode()).hexdigest()


async def create_user(db: Session, user: UserCreate = None) -> Optional[User]:

    # create new user
    user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role,
        phone=user.phone,
        firstname=user.firstname,
        lastname=user.lastname,
    )

    db.add(user)
    await db.flush()  # Get user.id

    return user


# def get_user(db: Session = Depends(get_db), user_id: UUID = None) -> Optional[Users]:
#     # db.get works with primary key types including UUID
#     return db.get(Users, user_id)


# def update_user(
#     db: Session = Depends(get_db), user_id: UUID = None, user: UserUpdate = None
# ) -> Optional[Users]:
#     db_user = db.get(Users, user_id)
#     if not db_user:
#         return None
#     if user.username is not None:
#         db_user.username = user.username
#     if user.email is not None:
#         db_user.email = user.email
#     if user.password is not None:
#         db_user.hashed_password = _hash_password(user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def delete_user(db: Session = Depends(get_db), user_id: UUID = None) -> bool:
#     db_user = db.get(Users, user_id)
#     if not db_user:
#         return False
#     db.delete(db_user)
#     db.commit()
#     return True
