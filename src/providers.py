from dishka import Provider, provide, Scope
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker
from typing import AsyncGenerator
from dishka import make_async_container

class DbProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def provide_postgres(self) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            yield session
            session.close()

container = make_async_container(DbProvider())