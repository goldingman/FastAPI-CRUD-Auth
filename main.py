from fastapi import FastAPI
from middleware.article import router as article_router
from middleware.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(article_router)


@app.get('/')
def welcome():
    """Welcome endpoint."""
    return {'message': 'Welcome to my FastAPI application'}