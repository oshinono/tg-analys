from dishka import Provider, provide, Scope
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import AsyncGenerator
from dishka import make_async_container
from sqlalchemy.exc import DBAPIError

class DbProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def provide_postgres(self) -> AsyncGenerator[AsyncSession, None]:
        async for session in get_async_session():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

container = make_async_container(DbProvider())