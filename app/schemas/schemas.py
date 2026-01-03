# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # 'student'|'landlord'|'admin'
    firstname: str
    lastname: str
    phone: str
    gender: str
    is_verified: Optional[bool] = False

    # Optional fields for student profile
    student_id: str
    university: str
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    preferred_location: Optional[str] = None
    preferred_room_type: Optional[str] = None
    preferred_amenities: Optional[List[str]] = None


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


class Login(BaseModel):
    email: EmailStr
    password: str


class PropertyCreate(BaseModel):
    title: str
    landlord_id: UUID
    description: Optional[str]
    location_text: Optional[str]
    price: float
    type: Optional[str] = "hostel"
    is_available: Optional[bool] = True


class ChatMessageIn(BaseModel):
    session_id: Optional[int]
    text: str


class RecommendationCard(BaseModel):
    property_id: int
    title: str
    price: float
    image_url: Optional[str]
    ai_score: float
    short_description: Optional[str]


class StudentProfile(BaseModel):
    user_id: UUID
    university: str
    student_id: str


# -----------------
# Search schemas
# -----------------
class SearchRequest(BaseModel):
    query: str
    max_price: Optional[float] = None


class SearchResult(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    price: Optional[float]
    score: float

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    results: List[SearchResult]


# -----------------
# Interaction schemas
# -----------------
class InteractionRequest(BaseModel):
    property_id: UUID
    event_type: str  # 'view', 'click', 'save', 'skip', etc.


class InteractionData(BaseModel):
    user_id: UUID
    property_id: UUID
    event_type: str

    class Config:
        from_attributes = True


class InteractionResponse(BaseModel):
    message: str
    interaction: InteractionData


# -----------------
# Recommendation schemas
# -----------------
class RecommendationProperty(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    price: Optional[float]

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    recommendations: Optional[List[RecommendationProperty]] = None
    message: Optional[str] = None


class TrainingResponse(BaseModel):
    task_id: str
    status: str


# -----------------
# Recommendation schemas
# -----------------
class RecommendationRequest(BaseModel):
    student_id: UUID


class PropertySummary(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    price: Optional[float]

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    message: Optional[str] = None
    recommendations: Optional[List[PropertySummary]] = None
