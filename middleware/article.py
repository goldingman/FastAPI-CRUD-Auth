from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.article import Article, ArticleCreate, ArticleResponse
from models.user import UserDB
from middleware.auth import get_current_user
from database.config import get_db


__all__ = ['router']


router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)


@router.get("/", response_model=List[ArticleResponse])
async def read_articles(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Retrieve all articles."""
    return db.query(Article).all()


@router.post("/", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Create a new article."""
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Update an article by ID."""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")

    for key, value in article.dict().items():
        setattr(db_article, key, value)

    db.commit()
    db.refresh(db_article)
    return db_article


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    """Delete an article by ID."""
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(db_article)
    db.commit()
    return {"message": "Article deleted"}