import uuid
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tada.src.api.models import Article
from tada.src.api.v1.schemas import ArticlePayload, ArticleResponse
from tada.src.database.models import DatabaseRepository
from tada.src.database.session import get_db_session, get_repository

router = APIRouter()

ArticleRepository = Annotated[
    DatabaseRepository[Article],
    Depends(get_repository(Article)),
]


@router.get("/posts")
async def get_articles(
    session: AsyncSession = Depends(get_db_session),
) -> list[ArticleResponse]:
    articles = await session.scalars(select(Article))
    return [ArticleResponse.model_validate(article) for article in articles]


@router.post("/posts")
async def create_article(
    payload: ArticlePayload, repository: ArticleRepository
) -> ArticleResponse:
    article = await repository.create(payload.model_dump())
    return ArticleResponse.model_validate(article)


@router.delete("/posts/{article_id}")
async def delete_article(
    article_id: uuid.UUID, repository: ArticleRepository
) -> dict[str, bool]:
    await repository.delete(article_id)
    return {"ok": True}


@router.put("/posts/{article_id}")
async def update_article(
    article_id: uuid.UUID, payload: ArticlePayload, repository: ArticleRepository
) -> ArticleResponse:
    article = await repository.update(pk=article_id, data=payload.model_dump())
    return article
