from aiogram.filters import Filter
from sqlalchemy.ext.asyncio import AsyncSession
from providers import container
from typing import AsyncGenerator

class BaseDbFilter(Filter):
    async def _get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with container() as c:
            session = await c.get(AsyncSession)
            yield session