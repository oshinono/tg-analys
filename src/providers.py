from dishka import Provider, provide, Scope
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from typing import AsyncGenerator
from dishka import make_async_container
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError, UserAlreadyParticipantError, 
    InviteHashExpiredError, UserDeactivatedBanError, 
    AuthKeyUnregisteredError, InviteHashInvalidError,
    ChannelPrivateError, SessionPasswordNeededError,
    SessionRevokedError, TypeNotFoundError,
    AuthKeyError, UnauthorizedError,
    UserPrivacyRestrictedError, UserIdInvalidError,
    InputUserDeactivatedError
)
from telethon.sessions import StringSession
import os

from loguru import logger

from config import settings

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

class TelethonProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_telethon(self) -> TelegramClient:
        try:
            session_file = os.path.join(os.path.dirname(__file__), 'tg.session')
            client = TelegramClient(
                session=session_file,
                api_id=settings.tg_api_id,
                api_hash=settings.tg_api_hash,
                device_model='OPPO Find X3 Pro',
                system_version='14.8.1',
                app_version='8.9',
                lang_code='ru',
                system_lang_code='ru-ru'
            )
            try:
                await client.connect()
            except Exception as e:
                logger.error(f"Ошибка подключения: {str(e)}")
                raise

            try:
                me = await client.get_me()
            except (AuthKeyUnregisteredError, SessionRevokedError, 
                    UserDeactivatedBanError, SessionPasswordNeededError,
                    TypeNotFoundError, AuthKeyError, UnauthorizedError) as e:
                logger.error(str(e))
                raise

            logger.info(f'Успешно логин через Telethon: {me.username}')

            return client
        except Exception as e:
            logger.error(str(e))
            raise
        

container = make_async_container(DbProvider(), TelethonProvider())