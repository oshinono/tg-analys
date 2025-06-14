from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_confirm_prompt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да, все хорошо ✅", callback_data="confirm_prompt")],
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")]
        ]
    )

async def get_prompt_keyboard(is_used: bool) -> InlineKeyboardMarkup:
    dynamic_button = InlineKeyboardButton(text="Применить", callback_data="use_prompt") if not is_used else InlineKeyboardButton(text="Используется ✅", callback_data="deactivate_prompt")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [dynamic_button],
            [InlineKeyboardButton(text="❌", callback_data="delete_prompt")],
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")]
        ]
    )