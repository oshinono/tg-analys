from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

DB_HOST = settings.postgres_host
DB_PORT = settings.postgres_port
DB_USER = settings.postgres_user
DB_PASSWORD = settings.postgres_password
DB_NAME = settings.postgres_db

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DB_URL, pool_size=20, max_overflow=50, pool_timeout=30)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    pass
