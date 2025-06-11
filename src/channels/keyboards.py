from channels.models import Channel
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_channels_keyboards(channels: list[Channel]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    for channel in channels:
        data = f"{channel.__class__.__name__.lower()}_{channel.id}"
        b.add(InlineKeyboardButton(text=str(channel), callback_data=data))

    b.adjust(3, repeat=True)

    b.row(InlineKeyboardButton(text="➕", callback_data=f"add_new_channel"))
    b.row(InlineKeyboardButton(text="Обновить из Google Таблиц 📊", callback_data="update_from_google_table"))
    b.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="index"))

    return b.as_markup()

async def get_channel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌", callback_data="delete_channel")],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="channels")]
    ])