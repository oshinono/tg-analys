from aiogram import Router, F
from aiogram.types import CallbackQuery
from roles.enums import Roles
from aiogram.fsm.context import FSMContext
from users.service import UserService
from users.keyboards import get_users_keyboard, get_user_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot
from roles.service import RoleService
from roles.keyboards import get_roles_keyboards
from users.schemas import UserUpdate
from users.states import UserStates
from roles.filters import AccessFilter
from loguru import logger
from users.dependencies import check_event_initiator, check_same_roles_event

router = Router()
router.message.filter(AccessFilter(Roles.SUPERUSER))
router.callback_query.filter(AccessFilter(Roles.SUPERUSER))


@router.callback_query(F.data == "users")
async def list_users(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.clear()
    await state.set_state(UserStates.users)
    
    message_to_edit_id = callback.message.message_id

    await state.update_data(message_to_edit_id=message_to_edit_id)

    # page_number = await check_users_page(state, session, callback)
    # limit = 6
    # offset = limit * page_number - limit

    users = await UserService.get_all(session)

    await bot.edit_message_text(message_id=message_to_edit_id, 
                                chat_id=callback.message.chat.id, 
                                text="Все пользователи:",
                                reply_markup=await get_users_keyboard(users))

@router.callback_query(UserStates.users, F.data.startswith("user_"))
async def user_page(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.set_state(UserStates.user)
    
    message_id = await state.get_value("message_to_edit_id")

    user_id = await state.get_value("current_user_id")
    if not user_id:
        user_id = int(callback.data.split("_")[1])
        await state.update_data(current_user_id=user_id)
        

    user = await UserService.get_by_id(user_id, session)

    text = f"Пользователь: {user.username if user.username else user.first_name}\n"
    text += f"ID: {user.id}\n"
    text += f"Роль: {user.role.name}\n"
    text += f"Телефон: {user.phone_number}\n"
    text += f"Дата добавления в систему: {user.created_at}\n"
    text += f"Дата обновления: {user.updated_at}\n"

    await bot.edit_message_text(message_id=message_id, 
                                chat_id=callback.message.chat.id, 
                                text=text, 
                                reply_markup=await get_user_keyboard(user.role.name, user.id))
    
@router.callback_query(UserStates.user, F.data == "delete_user")
async def delete_user(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    user_id = int(await state.get_value("current_user_id"))

    if await check_event_initiator(user_id, callback):
        return
    
    if await check_same_roles_event(callback, user_id, session):
        return

    await UserService.delete(user_id, session)

    return await list_users(callback, state, session, bot)

@router.callback_query(UserStates.user, F.data.startswith("change_user_role_"))
async def change_user_role(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.set_state(UserStates.change_user_role)
    
    message_id = await state.get_value("message_to_edit_id")
    user_id = int(callback.data.split("_")[3])
    await state.update_data(current_user_id=user_id)

    user = await UserService.get_by_id(user_id, session)
    roles = await RoleService.get_all(session)

    text = f"Выберите новую роль для пользователя {user.username if user.username else user.first_name}\n\n"
    text += f"Текущая роль: <b>{user.role.name}</b>"

    await bot.edit_message_text(message_id=message_id, 
                                chat_id=callback.message.chat.id, 
                                text=text, 
                                reply_markup=await get_roles_keyboards(roles))
    
@router.callback_query(UserStates.change_user_role, F.data == "back")
async def change_user_role_back(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    return await user_page(callback=callback, state=state, session=session, bot=bot)
    
@router.callback_query(UserStates.change_user_role, F.data.startswith("role_"))
async def change_user_role_last(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    role_id = callback.data.split("_")[1]
    user_id = int(await state.get_value("current_user_id"))

    if await check_event_initiator(user_id, callback):
        return
    
    if await check_same_roles_event(callback, user_id, session):
        return


    await UserService.update(user_id, UserUpdate(role_guid=role_id), session)

    return await user_page(callback, state, session, bot)
