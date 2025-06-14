from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from database import async_session_maker, RedisClient
from telethon import TelegramClient
from config import settings
import uuid

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with async_session_maker() as session:
            data["session"] = session
            return await handler(event, data)
        
class RedisClientMiddleware(BaseMiddleware):
    def __init__(self):
        self.redis_client = RedisClient()
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["redis"] = self.redis_client
        return await handler(event, data)
    
class TelethonClientMiddleware(BaseMiddleware):
    def __init__(self, telethon: TelegramClient):
        self.telethon = telethon
        
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["telethon"] = self.telethon
        return await handler(event, data)
