from typing import Generic, TypeVar

import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import fuzzy

from tada.src.api.models import Article, Status

T = TypeVar("T")


class BaseFactory(Generic[T], AsyncSQLAlchemyFactory):
    @classmethod
    async def create(cls, **kwargs) -> T:
        return await super().create(**kwargs)

    @classmethod
    async def create_batch(cls, *args, **kwargs) -> list[T]:
        return await super().create_batch(*args, **kwargs)


class ArticleFactory(BaseFactory[Article]):
    title = factory.Faker("sentence")
    content = factory.Faker("text")
    status = fuzzy.FuzzyChoice(choices=[Status.DRAFT, Status.PUBLISHED])

    class Meta:
        model = Article
        sqlalchemy_session_persistence = "commit"
