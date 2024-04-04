from collections.abc import AsyncGenerator
from typing import Callable

from fastapi import Depends
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from tada.src.database.models import Base, DatabaseRepository, async_engine


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    factory = async_sessionmaker(async_engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise


def get_repository(
    model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_db_session)):
        return DatabaseRepository(model, session)

    return func
