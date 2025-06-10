from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from roles.filters import UserFilter

router = Router()
router.message.filter(UserFilter())
router.callback_query.filter(UserFilter())

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот для анализа постов в Telegram. Если ты тут, значит ты есть в списке")