import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from telethon import TelegramClient
from config import settings
from consts import default_bot_settings, ALLOWED_UPDATES
from cmnds import commands
from loguru import logger
from utils import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from roles.init import add_user_role_to_db
from users.init import add_superusers_to_db
from providers import container
from router import router as index_router
from users.router import router as users_router
from channels.router import router as channels_router
from prompts.router import router as prompts_router
from moderation.router import router as moderation_router
from middlewares import DbSessionMiddleware, RedisClientMiddleware, TelethonClientMiddleware
from database import REDIS_URL

async def init():
    setup_logger()
    async with container() as c:
        session = await c.get(AsyncSession)
        await add_user_role_to_db(session)
        await add_superusers_to_db(session)

async def main():
    await init()
    storage = RedisStorage.from_url(REDIS_URL)
        
    async with Bot(token=settings.token, default=default_bot_settings, storage=storage) as bot:
        await bot.set_my_commands(commands)
        await bot.delete_webhook(drop_pending_updates=True)
        try:
            dp: Dispatcher = Dispatcher(storage=storage)
            dp.include_routers(index_router, users_router, channels_router, prompts_router, moderation_router)
        
            
            dp.update.middleware.register(DbSessionMiddleware())
            dp.update.middleware.register(RedisClientMiddleware())

            telethon = await container.get(TelegramClient)
            dp.update.middleware.register(TelethonClientMiddleware(telethon))

            # setup_dishka(container=container, router=dp)

            bot_info = await bot.get_me()
            logger.info(f"Бот запущен | {bot_info.full_name}, @{bot_info.username} | {bot_info.url}")

            await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
        finally:
            await dp.stop_polling()
            await dp.storage.close()
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())