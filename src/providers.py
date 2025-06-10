from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from dishka import make_async_container

class DbProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_postgres(self) -> AsyncSession:
        return await get_async_session()
    
