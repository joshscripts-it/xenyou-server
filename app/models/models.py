# app/models.py

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

from app.schemas.schemas import StudentProfile


# ===================
# Core Identity
# ===================


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(nullable=False)
    is_verified: Optional[bool] = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=False)

    # Relationships (forward references as strings)
    student_profile: Optional["StudentProfile"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    landlord_profile: Optional["LandlordProfile"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    admin_profile: Optional["AdminProfile"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    # verification: Optional["Verification"]

    chat_sessions: List["ChatSession"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    search_queries: List["SearchQuery"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    interactions: List["InteractionEvent"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    recommendations: List["Recommendation"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    saved_properties: List["SavedProperty"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    matches: List["Match"] = Relationship(back_populates="user", cascade_delete=True)


# ===================
# Student profile
# ===================
class StudentProfile(SQLModel, table=True):
    __tablename__ = "student_profiles"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)

    gender: Optional[str] = None
    university: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    preferred_location: Optional[str] = None
    preferred_room_type: Optional[str] = None
    preferred_amenities: Optional[dict] = Field(default=None, sa_type=JSON)
    student_id: str = Field(unique=True, nullable=False)

    embedding_vector: Optional[list] = Field(default=None, sa_type=JSON)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    verification: Optional["StudentVerification"] = Relationship(
        back_populates="student", cascade_delete=True
    )
    user: Optional["User"] = Relationship(
        back_populates="student_profile", cascade_delete=True
    )


# ===================
# Landlord profile
# ===================
class LandlordProfile(SQLModel, table=True):
    __tablename__ = "landlord_profiles"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)

    verified: bool = Field(default=False)
    verification_info: Optional[dict] = Field(default=None, sa_type=JSON)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    # relationships
    user: Optional["User"] = Relationship(
        back_populates="landlord_profile", cascade_delete=True
    )
    properties: List["Property"] = Relationship(
        back_populates="landlord", cascade_delete=True
    )
    verification: Optional["LandlordVerification"] = Relationship(
        back_populates="landlord", cascade_delete=True
    )


# ===================
# Admin profile
# ===================
class AdminProfile(SQLModel, table=True):
    __tablename__ = "admin_profiles"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)

    role_level: Optional[str] = None

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="admin_profile")
    verification: Optional["AdminVerification"] = Relationship(
        back_populates="admin", cascade_delete=True
    )


class LandlordVerification(SQLModel, table=True):
    __tablename__ = "landlord_verifications"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    landlord_id: Optional[UUID] = Field(
        default=None, foreign_key="landlord_profiles.id", nullable=True
    )
    id_type: str = Field(nullable=False)  # e.g. 'NIN', 'CAC'
    document_url: str = Field(nullable=False)
    verified: bool = Field(default=False)
    verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    landlord: Optional["LandlordProfile"] = Relationship(
        back_populates="verification", cascade_delete=True
    )


class StudentVerification(SQLModel, table=True):
    __tablename__ = "student_verifications"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    student_id: UUID = Field(foreign_key="student_profiles.id")
    id_type: str = Field(nullable=False)  # e.g. 'Student ID Card'
    document_url: str = Field(nullable=False)
    verified: bool = Field(default=False)
    verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    student: Optional["StudentProfile"] = Relationship(
        back_populates="verification", cascade_delete=True
    )


class AdminVerification(SQLModel, table=True):
    __tablename__ = "admin_verifications"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    admin_id: UUID = Field(foreign_key="admin_profiles.id")
    id_type: str = Field(nullable=False)  # e.g. 'Government ID', 'Admin Credentials'
    document_url: str = Field(nullable=False)
    verified: bool = Field(default=False)
    verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    admin: Optional["AdminProfile"] = Relationship(
        back_populates="verification", cascade_delete=True
    )


# ===========================
# Properties (multi-property)
# ===========================
class Property(SQLModel, table=True):
    __tablename__ = "properties"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    landlord_id: UUID = Field(foreign_key="landlord_profiles.id")

    title: str = Field(nullable=False, unique=True)
    description: Optional[str] = None

    location_text: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

    price: Optional[int] = None
    type: Optional[str] = None
    gender_restriction: Optional[str] = None
    is_available: bool = Field(default=True)
    pet_owner: Optional[bool] = None
    move_in_date: Optional[datetime] = None
    rent_duration: Optional[str] = None

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    # relationships
    landlord: Optional["LandlordProfile"] = Relationship(
        back_populates="properties", cascade_delete=True
    )
    images: List["PropertyImage"] = Relationship(
        back_populates="property", cascade_delete=True
    )
    features: Optional["PropertyFeature"] = Relationship(
        back_populates="property", cascade_delete=True
    )
    interactions: List["InteractionEvent"] = Relationship(
        back_populates="property", cascade_delete=True
    )
    recommendations: List["Recommendation"] = Relationship(
        back_populates="property", cascade_delete=True
    )


class PropertyImage(SQLModel, table=True):
    __tablename__ = "property_images"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    property_id: UUID = Field(foreign_key="properties.id")

    image_url: str = Field(nullable=False)

    property: Optional["Property"] = Relationship(
        back_populates="images", cascade_delete=True
    )


# ===================
# Property features
# ===================
class PropertyFeature(SQLModel, table=True):
    __tablename__ = "property_features"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    property_id: UUID = Field(foreign_key="properties.id", unique=True)

    amenities: Optional[dict] = Field(default=None, sa_type=JSON)
    rules: Optional[dict] = Field(default=None, sa_type=JSON)
    near_landmarks: Optional[dict] = Field(default=None, sa_type=JSON)
    furnishing_level: Optional[str] = None
    rating_score: Optional[float] = None

    embedding_vector: Optional[list] = Field(default=None, sa_type=JSON)

    property: Optional["Property"] = Relationship(
        back_populates="features", cascade_delete=True
    )


# ===================
# Chat / sessions / messages
# ===================
class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_sessions"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")

    session_state: Optional[dict] = Field(default=None, sa_type=JSON)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(
        back_populates="chat_sessions", cascade_delete=True
    )
    messages: List["ChatMessage"] = Relationship(
        back_populates="session", cascade_delete=True
    )


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="chat_sessions.id")

    sender: Optional[str] = None
    message_text: Optional[str] = None
    intent: Optional[str] = None
    embedding_vector: Optional[list] = Field(default=None, sa_type=JSON)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    session: Optional["ChatSession"] = Relationship(
        back_populates="messages", cascade_delete=True
    )


# ===================
# Search & rec history
# ===================
class SearchQuery(SQLModel, table=True):
    __tablename__ = "search_queries"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")

    search_text: Optional[str] = None
    structured_filters: Optional[dict] = Field(default=None, sa_type=JSON)
    embedding_vector: Optional[list] = Field(default=None, sa_type=JSON)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(
        back_populates="search_queries", cascade_delete=True
    )


# ===================
# Recommendations
# ===================
class Recommendation(SQLModel, table=True):
    __tablename__ = "recommendations"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    property_id: UUID = Field(foreign_key="properties.id")

    ai_score: Optional[float] = None
    rank_position: Optional[int] = None

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(
        back_populates="recommendations", cascade_delete=True
    )
    property: Optional["Property"] = Relationship(
        back_populates="recommendations", cascade_delete=True
    )


# ===================
# Interaction events (view/click/save/skip)
# ===================
class InteractionEvent(SQLModel, table=True):
    __tablename__ = "interaction_events"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    property_id: UUID = Field(foreign_key="properties.id")

    event_type: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(
        back_populates="interactions", cascade_delete=True
    )
    property: Optional["Property"] = Relationship(
        back_populates="interactions", cascade_delete=True
    )


# ===================
# Saved properties
# ===================
class SavedProperty(SQLModel, table=True):
    __tablename__ = "saved_properties"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    property_id: UUID = Field(foreign_key="properties.id")

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(
        back_populates="saved_properties", cascade_delete=True
    )


# ===================
# Matches
# ===================
class Match(SQLModel, table=True):
    __tablename__ = "matches"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    property_id: UUID = Field(foreign_key="properties.id")

    match_score: Optional[float] = None
    matched_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="matches", cascade_delete=True)


# ===================
# Refresh tokens
# ===================
class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    token: str = Field(unique=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    revoked: bool = Field(default=False)
