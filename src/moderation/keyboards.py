from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Base
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def get_moderation_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Промпты", callback_data="unapproved_prompts")],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="index")]
    ])
    
async def get_unapproved_keyboards(objects: list[Base], name: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    if objects:
        for object in objects:
            data = f"{name}_{getattr(object, 'id', None) or getattr(object, 'guid')}"
            b.add(InlineKeyboardButton(text=str(object), callback_data=data))

        b.adjust(3, repeat=True)

    b.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="back"))

    return b.as_markup()

async def get_unapproved_prompt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅", callback_data="approve_prompt"), InlineKeyboardButton(text="❌", callback_data="reject_prompt")],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")]
    ])

