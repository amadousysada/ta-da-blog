from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tada.src.api.models import Article

from .factories import ArticleFactory


async def test_create_article(api_client: AsyncClient, db_session: AsyncSession):
    article = ArticleFactory.build()

    # Assert that no article exists in Database
    articles = await db_session.scalars(select(Article))
    assert len(articles.all()) == 0

    payload = {
        "title": article.title,
        "status": article.status.value,
        "content": article.content,
    }
    response = await api_client.post("v1/posts", json=payload)

    assert response.status_code == 200

    # Assert that one article has been created in Database
    articles = await db_session.scalars(select(Article))
    assert len(articles.all()) == 1

    res_json = response.json()

    assert res_json["title"] == payload["title"]
    assert res_json["status"] == payload["status"]
    assert res_json["content"] == payload["content"]


async def test_get_articles(api_client: AsyncClient, db_session: AsyncSession):
    # Create 10 articles
    await ArticleFactory.create_batch(10)

    # Assert that all 10 articles have been created
    articles = await db_session.scalars(select(Article))
    assert len(articles.all()) == 10

    response = await api_client.get("v1/posts")

    assert response.status_code == 200
    assert len(response.json()) == 10


async def test_delete_article(api_client: AsyncClient, db_session: AsyncSession):
    # Create 2 articles
    await ArticleFactory.create_batch(2)

    # Assert that all 2 articles have been created
    articles = await db_session.scalars(select(Article))
    articles = articles.all()
    assert len(articles) == 2

    response = await api_client.delete(f"v1/posts/{articles[0].id}")

    assert response.status_code == 200
    assert response.json()["ok"]

    # Assert that only 1 article remain in Database
    articles = await db_session.scalars(select(Article))
    assert len(articles.all()) == 1


async def test_update_article(api_client: AsyncClient, db_session: AsyncSession):
    # Create 1 article
    await ArticleFactory()

    # Assert that all 1 article has been created
    articles = await db_session.scalars(select(Article))
    articles = articles.all()
    assert len(articles) == 1
    old_article = articles[0]

    old_id = old_article.id
    old_update_at = old_article.updated_at
    old_created = old_article.created_at
    old_title = old_article.title
    old_content = old_article.content
    old_status = old_article.status

    payload = {
        "title": "new title",
        "content": "new content lorem ipsum dolor....",
        "status": "published" if old_article.status.value == "draft" else "draft",
    }

    response = await api_client.put(f"v1/posts/{old_article.id}", json=payload)

    res_json = response.json()

    assert res_json["id"] == str(old_id)
    assert res_json["created_at"] == old_created.strftime("%Y-%m-%dT%H:%M:%S.%f")

    assert res_json["title"] != old_title
    assert res_json["content"] != old_content
    assert res_json["updated_at"] != old_update_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert res_json["status"] != old_status
