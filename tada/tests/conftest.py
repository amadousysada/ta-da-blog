from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from tada.src.database.models import Base, async_engine
from tada.src.database.session import get_db_session
from tada.src.main import app

from .factories import ArticleFactory

factory_list = [ArticleFactory]


@pytest.fixture(scope="session", autouse=True)
async def db_connection() -> None:
    """
    Fixture to create database tables from scratch for each test session.
    """
    # always drop and create test DB tables between test sessions
    async with async_engine.connect() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def db_session():
    async with async_engine.connect() as conn:
        await conn.begin()
        async_session = async_sessionmaker(bind=conn)()

        for factory in factory_list:
            factory._meta.sqlalchemy_session = async_session

        yield async_session
        await async_session.commit()
        await async_session.close()


@pytest.fixture(scope="function")
async def api_client(db_session) -> AsyncGenerator[AsyncClient, None]:
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://localhost:8001") as client:
        yield client
