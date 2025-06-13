from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_confirm_prompt_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Да, все хорошо ✅", callback_data="confirm_prompt")],
            [InlineKeyboardButton(text="Назад ⬅️", callback_data="back")]
        ]
    )