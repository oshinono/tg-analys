from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_index_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пользователи 👥", callback_data="users")]
        ]
    )

async def get_simple_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")]
        ]
    )

async def get_default_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")],
            [InlineKeyboardButton(text="Главная 🔙", callback_data="index")]
        ]
    )
