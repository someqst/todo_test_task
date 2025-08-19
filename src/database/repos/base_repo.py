from typing import TypeVar, Type
from abc import ABC, abstractmethod
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class IRepository(ABC):
    @abstractmethod
    async def add_one():
        pass

    @abstractmethod
    async def get_by_id():
        pass

    @abstractmethod
    async def get_all():
        pass

    @abstractmethod
    async def get_all_by_status():
        pass


class Repository(IRepository):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_id(self, id: str):
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()
