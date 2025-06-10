from aiogram.filters import Filter
from sqlalchemy.ext.asyncio import AsyncSession
from providers import container

class BaseDbFilter(Filter):
    async def _get_session(self) -> AsyncSession:
        async with container() as c:
            session = await c.get(AsyncSession)
            return session
    