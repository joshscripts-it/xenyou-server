# app/models.py

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime


# ===================
# Core Identity
# ===================


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    email: str = Field(index=True, nullable=False)
    password_hash: str = Field(nullable=False)
    role: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, nullable=False)

    # Relationships (forward references as strings)
    student_profile: Optional["StudentProfile"] = Relationship(back_populates="user")
    landlord_profile: Optional["LandlordProfile"] = Relationship(back_populates="user")
    admin_profile: Optional["AdminProfile"] = Relationship(back_populates="user")

    chat_sessions: List["ChatSession"] = Relationship(back_populates="user")
    search_queries: List["SearchQuery"] = Relationship(back_populates="user")
    interactions: List["InteractionEvent"] = Relationship(back_populates="user")
    recommendations: List["Recommendation"] = Relationship(back_populates="user")
    saved_properties: List["SavedProperty"] = Relationship(back_populates="user")
    matches: List["Match"] = Relationship(back_populates="user")


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

    user: Optional["User"] = Relationship(back_populates="student_profile")


# ===================
# Landlord profile
# ===================
class LandlordProfile(SQLModel, table=True):
    __tablename__ = "landlord_profiles"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)

    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    verified: bool = Field(default=False)
    verification_info: Optional[dict] = Field(default=None, sa_type=JSON)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="landlord_profile")
    properties: List["Property"] = Relationship(back_populates="landlord")


# ===================
# Admin profile
# ===================
class AdminProfile(SQLModel, table=True):
    __tablename__ = "admin_profiles"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)

    full_name: Optional[str] = None
    role_level: Optional[str] = None

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="admin_profile")


# ===================
# Properties (multi-property)
# ===================
class Property(SQLModel, table=True):
    __tablename__ = "properties"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    landlord_id: UUID = Field(foreign_key="landlord_profiles.id")

    title: str = Field(nullable=False)
    description: Optional[str] = None

    location_text: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None

    price: Optional[int] = None
    type: Optional[str] = None
    gender_restriction: Optional[str] = None
    is_available: bool = Field(default=True)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    landlord: Optional["LandlordProfile"] = Relationship(back_populates="properties")
    images: List["PropertyImage"] = Relationship(
        back_populates="property", cascade_delete=True
    )
    features: Optional["PropertyFeature"] = Relationship(back_populates="property")
    interactions: List["InteractionEvent"] = Relationship(back_populates="property")
    recommendations: List["Recommendation"] = Relationship(back_populates="property")


class PropertyImage(SQLModel, table=True):
    __tablename__ = "property_images"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    property_id: UUID = Field(foreign_key="properties.id")

    image_url: str = Field(nullable=False)

    property: Optional["Property"] = Relationship(back_populates="images")


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

    property: Optional["Property"] = Relationship(back_populates="features")


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

    user: Optional["User"] = Relationship(back_populates="chat_sessions")
    messages: List["ChatMessage"] = Relationship(back_populates="session")


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="chat_sessions.id")

    sender: Optional[str] = None
    message_text: Optional[str] = None
    intent: Optional[str] = None
    embedding_vector: Optional[list] = Field(default=None, sa_type=JSON)

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    session: Optional["ChatSession"] = Relationship(back_populates="messages")


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

    user: Optional["User"] = Relationship(back_populates="search_queries")


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

    user: Optional["User"] = Relationship(back_populates="recommendations")
    property: Optional["Property"] = Relationship(back_populates="recommendations")


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

    user: Optional["User"] = Relationship(back_populates="interactions")
    property: Optional["Property"] = Relationship(back_populates="interactions")


# ===================
# Saved properties
# ===================
class SavedProperty(SQLModel, table=True):
    __tablename__ = "saved_properties"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    property_id: UUID = Field(foreign_key="properties.id")

    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="saved_properties")


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

    user: Optional["User"] = Relationship(back_populates="matches")


# ===================
# Refresh tokens
# ===================
class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    token: str = Field(unique=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    expires_at: datetime
    revoked: bool = Field(default=False)
