from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from users.models import User
from roles.models import Role

async def get_users_keyboard(users: list[User]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    for user in users:
        b.add(InlineKeyboardButton(text=user.username if user.username else user.first_name, callback_data=f"user_{user.id}"))
    
    b.adjust(2, repeat=True)
    
    b.row(InlineKeyboardButton(text="➕", callback_data="add_new_user"))
    b.row(InlineKeyboardButton(text="Назад ⬅️", callback_data="index"))

    return b.as_markup()

async def get_user_keyboard(user_role: str, user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=user_role, callback_data=f"change_user_role_{user_id}"), InlineKeyboardButton(text=" ", callback_data=" "), InlineKeyboardButton(text="❌", callback_data="delete_user")],
        [InlineKeyboardButton(text="Назад ⬅️", callback_data="users")]
    ])
