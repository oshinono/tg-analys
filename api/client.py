from telethon import TelegramClient
from config import settings

client = TelegramClient('session_name', settings.tg_api_id, settings.tg_api_hash)

async def get_telegram_client():
    async with client:
        yield client