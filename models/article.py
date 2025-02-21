"""Article models for database and API schemas."""
from sqlalchemy import Column, Integer, String, Float
# Pydantic models for request/response
from pydantic import BaseModel
from database.config import Base


class Article(Base):
    """Database model for articles."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    price = Column(Float)


class ArticleBase(BaseModel):
    """Base schema for article information."""
    name: str
    price: float


class ArticleCreate(ArticleBase):
    """Schema for creating article."""
    pass


class ArticleResponse(ArticleBase):
    """Schema for article response."""
    id: int


class Config:
    """Configure Pydantic to read ORM objects."""
    orm_mode = True
