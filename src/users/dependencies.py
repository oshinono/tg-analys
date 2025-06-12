from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from users.service import UserService

async def check_users_page(state: FSMContext, session: AsyncSession, callback: CallbackQuery):
    data = await state.get_data()

    page_number = data.get("users_page_number")

    if page_number is None:
        await state.update_data(users_page_number=1)
        page_number = 1
        

    if callback.data == "users_next_page":
        page_number += 1
    elif callback.data == "users_previous_page":
        page_number -= 1
    
    message_to_edit_id = data.get("message_to_edit_id")

    if message_to_edit_id is None:
        await state.update_data(message_to_edit_id=callback.message.message_id)

    return page_number

async def get_users_count(session: AsyncSession):
    return await len(UserService.get_all(session))

async def check_event_initiator(current_user_id: int, callback: CallbackQuery) -> bool:
    if current_user_id == callback.from_user.id:
        await callback.answer(text="Вы не можете изменять самого себя.", show_alert=True)
        return True
    return False

async def check_same_roles_event(callback: CallbackQuery, user_id: int, session: AsyncSession) -> bool:
    initiator = await UserService.get_by_id(callback.from_user.id, session)
    user = await UserService.get_by_id(user_id, session)

    if initiator.role.permission_level <= user.role.permission_level:
        await callback.answer(text="У вас нет прав для этого действия.", show_alert=True)
        return True
    return False
