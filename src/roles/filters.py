from aiogram.filters import Filter
from aiogram.types import Message
from config import settings
from filters import BaseDbFilter
from aiogram import Bot
from users.service import UserService

class UserFilter(BaseDbFilter):

    async def __call__(self, event, bot: Bot) -> bool:
        user_id: int = event.from_user.id

        user = await UserService.get_by_id(user_id, await self._get_session())
        if not user:
            return False
        
        return True