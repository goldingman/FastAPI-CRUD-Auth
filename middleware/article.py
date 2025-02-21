from typing import List

from fastapi import APIRouter, Depends
from models.article import Article
from middleware.auth import get_current_user, User


__all__ = ['router']


router = APIRouter(
    prefix="/articles",
    tags=["articles"]
)

articles = []


@router.get("/", response_model=List[Article])
async def read_articles(current_user: User = Depends(get_current_user)):
    """Retrieve all articles."""
    return articles


@router.post("/", response_model=Article)
async def create_article(
    article: Article,
    current_user: User = Depends(get_current_user)
):
    """Create a new article."""
    articles.append(article)
    return article


@router.put("/{article_id}", response_model=Article)
async def update_article(
    article_id: int,
    article: Article,
    current_user: User = Depends(get_current_user)
):
    """Update an article by ID."""
    articles[article_id] = article
    return article


@router.delete("/{article_id}")
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_user)
):
    """Delete an article by ID."""
    del articles[article_id]
    return {"message": "Article deleted"} 