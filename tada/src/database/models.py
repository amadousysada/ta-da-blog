import uuid
from typing import Generic, TypeVar

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from tada.src.config import get_settings

Base = declarative_base()

async_engine = create_async_engine(get_settings().get_db_url())

Model = TypeVar("Model")


class DatabaseRepository(Generic[Model]):
    def __init__(self, model: type(Model), async_session: AsyncSession) -> None:
        self.model = model
        self.session = async_session

    async def create(self, data: dict) -> Model:
        instance = self.model(**data)
        self.session.add(instance=instance)
        await self.session.commit()
        await self.session.refresh(instance=instance)

        return instance

    async def delete(self, pk: uuid.UUID) -> dict:
        instance = await self.session.get(self.model, pk)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{self.model.name} not found")
        await self.session.delete(instance=instance)
        await self.session.commit()

    async def update(self, pk: uuid.UUID, data: dict):
        instance = await self.session.get(self.model, pk)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{self.model.name} not found")

        for key, value in data.items():
            setattr(instance, key, value)
        self.session.add(instance=instance)
        await self.session.commit()
        await self.session.refresh(instance)

        return instance
