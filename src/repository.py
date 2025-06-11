import uuid
from schemas import BaseCreate, BaseUpdate
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database import Base

class BaseRepository:
    model: Base = None

    @classmethod
    async def get_all(cls, session: AsyncSession, limit: int = 10, offset: int = 0, **filter_by) -> list[Base]:            
        query = select(cls.model).filter_by(**filter_by).offset(offset).limit(limit)
        result = await session.execute(query)
        scalars = result.scalars().all()
        return scalars
    
    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by) -> Base | None:
        result = await session.execute(select(cls.model).filter_by(**filter_by))
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_by_id(cls, id: uuid.UUID | int, session: AsyncSession) -> Base | None:
        result = await session.execute(select(cls.model).where(cls.model.id == id))
        return result.scalar_one_or_none()
    
    @classmethod
    async def create(cls, data: BaseCreate, session: AsyncSession) -> Base:
        query = insert(cls.model).values(**data.model_dump()).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalar_one()
    
    @classmethod
    async def create_all(cls, data: list[BaseCreate], session: AsyncSession) -> list[Base]:
        query = insert(cls.model).values([data.model_dump() for data in data]).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalars().all()
    
    @classmethod
    async def update(cls, id: uuid.UUID | int, data: BaseUpdate, session: AsyncSession) -> Base:
        result = await session.execute(update(cls.model).where(cls.model.id == id).values(**data.model_dump(exclude_unset=True, exclude_none=True)).returning(cls.model))
        await session.commit()
        return result.scalar_one()
    
    @classmethod
    async def delete(cls, id: uuid.UUID | int, session: AsyncSession) -> bool:
        result = await session.execute(delete(cls.model).where(cls.model.id == id))
        await session.commit()
        return result.rowcount > 0