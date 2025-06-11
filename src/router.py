from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from roles.enums import Roles
from roles.filters import AccessFilter
from keyboards import get_index_keyboard

router = Router()
router.message.filter(AccessFilter(role=Roles.USER))
router.callback_query.filter(AccessFilter(role=Roles.USER))

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот для анализа постов в Telegram. Если ты тут, значит ты есть в списке",
                         reply_markup=await get_index_keyboard())
    
@router.callback_query(F.data == "index")
async def index_callback(callback: CallbackQuery):
    await callback.message.edit_text("Привет! Я бот для анализа постов в Telegram. Если ты тут, значит ты есть в списке",
                                    reply_markup=await get_index_keyboard())
