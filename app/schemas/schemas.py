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


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: str = "bearer"


class Login(BaseModel):
    email: EmailStr
    password: str


class PropertyCreate(BaseModel):
    title: str
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
