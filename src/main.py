import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config import settings
from consts import default_bot_settings, ALLOWED_UPDATES
from cmnds import commands
from loguru import logger
from dishka.integrations.aiogram import setup_dishka
from providers import DbProvider, make_async_container
from utils import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from roles.init import add_user_role_to_db
from users.init import add_superusers_to_db

async def main():
    storage = RedisStorage.from_url(f'redis://{settings.redis_user}:{settings.redis_password}@redis:{settings.redis_port}', connection_kwargs={"password": settings.redis_password})
    setup_logger()
    container = make_async_container(DbProvider())

    async with container() as c:
        session = await c.get(AsyncSession)
        await add_user_role_to_db(session)
        await add_superusers_to_db(session)

    async with Bot(token=settings.token, default=default_bot_settings, storage=storage) as bot:
        await bot.set_my_commands(commands)
        await bot.delete_webhook(drop_pending_updates=True)
        try:
            dp = Dispatcher(storage=storage)

            setup_dishka(container=container, router=dp, auto_inject=True)

            bot_info = await bot.get_me()
            logger.info(f"Бот запущен | {bot_info.full_name}, @{bot_info.username} | {bot_info.url}")

            await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
        finally:
            await dp.storage.close()
            await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())