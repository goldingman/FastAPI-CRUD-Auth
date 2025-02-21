"""User models for database and API schemas."""
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from database.config import Base


class UserDB(Base):
    """Database model for users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)


class UserBase(BaseModel):
    """Base schema for user information."""
    username: str
    email: str


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool


class Config:
    """Configure Pydantic to read ORM objects."""
    orm_mode = True
