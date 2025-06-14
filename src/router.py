from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from roles.enums import Roles
from roles.filters import AccessFilter
from keyboards import get_index_keyboard
from aiogram.fsm.context import FSMContext
from utils import clear_state


router = Router()
router.message.filter(AccessFilter(role=Roles.USER))
router.callback_query.filter(AccessFilter(role=Roles.USER))

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await clear_state(state)
    await message.answer("Привет! Я бот для анализа постов в Telegram. Если ты тут, значит ты есть в списке",
                         reply_markup=await get_index_keyboard())
    
@router.callback_query(F.data == "index")
async def index_callback(callback: CallbackQuery, state: FSMContext):
    await clear_state(state)
    await callback.message.edit_text("Привет! Я бот для анализа постов в Telegram. Если ты тут, значит ты есть в списке",
                                    reply_markup=await get_index_keyboard())

@router.callback_query(F.data == "delete_notification")
async def remove_noti(callback: CallbackQuery):
    await callback.message.delete()