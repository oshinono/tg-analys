from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from redis.asyncio import from_url, Redis
from config import settings
import json
from datetime import datetime
from consts import DATETIME_PATTERN

DB_HOST = settings.postgres_host
DB_PORT = settings.postgres_port
DB_USER = settings.postgres_user
DB_PASSWORD = settings.postgres_password
DB_NAME = settings.postgres_db

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
REDIS_URL = f'redis://default:{settings.redis_password}@redis:{settings.redis_port}'

engine = create_async_engine(DB_URL, pool_size=20, max_overflow=50, pool_timeout=30)

async_session_maker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

class Base(DeclarativeBase):
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if name in ('created_at', 'updated_at') and isinstance(value, datetime):
            return value.strftime(DATETIME_PATTERN)
        return value

class RedisClient:
    def __init__(self):
        self._redis_client = from_url(url=REDIS_URL, decode_responses=True)

    async def get_by_pattern(self, pattern: str) -> list[dict]:
        keys = await self._redis_client.keys(pattern)
        if not keys:
            return []
        values = await self._redis_client.mget(*keys)
        return [json.loads(value) for value in values]
    
    async def get(self, key: str) -> dict:
        value = await self._redis_client.get(key)
        return json.loads(value)
    
    async def set(self, key: str, value: dict, ttl: int | None = None) -> None:
        await self._redis_client.set(key, json.dumps(value), ex=ttl)
        
    async def delete(self, key: str) -> None:
        await self._redis_client.delete(key)