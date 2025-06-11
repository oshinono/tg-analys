from sqlalchemy.ext.asyncio import AsyncSession
from repository import BaseRepository
import uuid
from database import Base
from schemas import BaseCreate, BaseUpdate

class BaseService:

    repository: BaseRepository = None
    
    @classmethod
    async def get_by_id(cls, id: uuid.UUID | int, session: AsyncSession) -> Base:
        return await cls.repository.get_by_id(id, session)

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by) -> Base | None:
        return await cls.repository.get_one_or_none(session, **filter_by)
    
    @classmethod
    async def get_all(cls, session: AsyncSession, limit: int = 10, offset: int = 0, **filter_by) -> list[Base]:
        return await cls.repository.get_all(session, limit, offset, **filter_by)
    
    @classmethod
    async def create(cls, data: BaseCreate, session: AsyncSession) -> Base:
        return await cls.repository.create(data, session)
    
    @classmethod
    async def create_all(cls, data: list[BaseCreate], session: AsyncSession) -> list[Base]:
        return await cls.repository.create_all(data, session)
    
    @classmethod
    async def update(cls, id: uuid.UUID | int, data: BaseUpdate, session: AsyncSession) -> Base:
        return await cls.repository.update(id, data, session)
    
    @classmethod
    async def delete(cls, id: uuid.UUID | int, session: AsyncSession) -> bool:
        return await cls.repository.delete(id, session)