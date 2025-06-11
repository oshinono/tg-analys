from roles.models import Role
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_roles_keyboards(roles: list[Role]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    for role in roles:
        b.add(InlineKeyboardButton(text=role.name, callback_data=f"role_{role.guid}"))

    b.adjust(3, repeat=True)
    b.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="back"))

    return b.as_markup()