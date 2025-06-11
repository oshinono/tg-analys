from aiogram import Router, F, Bot
from roles.filters import AccessFilter
from roles.enums import Roles
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from channels.service import ChannelService
from sqlalchemy.ext.asyncio import AsyncSession
from channels.states import ChannelsStates
from channels.keyboards import get_channels_keyboards, get_channel_keyboard
from keyboards import get_simple_back_keyboard
from channels.schemas import ChannelCreate, ChannelUpdate
from loguru import logger
import uuid

router = Router()
router.message.filter(AccessFilter(Roles.ADMIN))
router.callback_query.filter(AccessFilter(Roles.ADMIN))

@router.callback_query(F.data == "channels")
async def list_channels(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.set_state(ChannelsStates.channels)
    channels = await ChannelService.get_all(session)

    message_to_edit_id = await state.get_value('message_to_edit_id')
    if not message_to_edit_id:
        message_to_edit_id = callback.message.message_id
        await state.update_data(message_to_edit_id=message_to_edit_id)

    await bot.edit_message_text(text="Все каналы:",
                                chat_id=callback.message.chat.id,
                                message_id=message_to_edit_id,
                                reply_markup=await get_channels_keyboards(channels))
    
@router.callback_query(F.data == "update_from_google_table")
async def parse_all_from_google_tables(callback: CallbackQuery, session: AsyncSession, state: FSMContext, bot: Bot):
    created_channels, updated_channels = await ChannelService.load_all_channels(session)
    await callback.answer(text=f"Добавлено: {len(created_channels)} каналов\nОбновлено: {len(updated_channels)} каналов",
                          show_alert=True)
    return await list_channels(callback, state, session, bot)

@router.callback_query(ChannelsStates.channels, F.data.startswith("channel_"))
async def channel_page(callback: CallbackQuery, session: AsyncSession, state: FSMContext, bot: Bot):
    await state.set_state(ChannelsStates.channel)
    message_to_edit_id = await state.get_value("message_to_edit_id")

    channel_id = int(callback.data.split("_")[1])

    channel = await ChannelService.get_by_id(channel_id, session)
    await state.update_data(current_channel_id=channel.id)

    text = f"ID: <code>{channel.id}</code>"
    text += f"\nНазвание: {channel.title}"
    text += f"\nЮзернейм: <code>{channel.username}</code>"
    text += f"\nСсылка: {channel.url}"

    await bot.edit_message_text(text=text,
                                reply_markup=await get_channel_keyboard(),
                                message_id=message_to_edit_id,
                                chat_id=callback.message.chat.id)


@router.callback_query(ChannelsStates.channel, F.data == "delete_channel")
async def delete_channel(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    channel_id = await state.get_value("current_channel_id")

    await ChannelService.delete(channel_id, session)
    return await list_channels(callback, state, session, bot)

@router.callback_query(ChannelsStates.channels, F.data == "add_new_channel")
async def add_new_channel(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.set_state(ChannelsStates.add_channel)

    message_to_edit_id = await state.get_value('message_to_edit_id')
    await bot.edit_message_text(text="Введите информацию в формате \n<code>ID Название Юзернейм Ссылка</code>",
                                chat_id=callback.message.chat.id,
                                message_id=message_to_edit_id,
                                reply_markup=await get_simple_back_keyboard())
    
@router.callback_query(ChannelsStates.add_channel, F.data == "back")
async def add_new_channel_back(callback: CallbackQuery, state: FSMContext, session: AsyncSession, bot: Bot):
    return await list_channels(callback, state, session, bot)

@router.message(ChannelsStates.add_channel)
async def add_new_channel_message(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    message_to_edit_id = await state.get_value('message_to_edit_id')
    await message.delete()
    
    data = message.text.split()
    if len(data) != 4:
        await bot.edit_message_text(text="Неверный формат. Попробуйте еще раз.\n\n<code>ID Название Юзернейм Ссылка</code>",
                                    chat_id=message.chat.id,
                                    message_id=message_to_edit_id,
                                    reply_markup=await get_simple_back_keyboard())
        return
    
    channel_id, title, username, url = data

    channel = await ChannelService.get_by_id(int(channel_id), session)
    if not channel:
        await ChannelService.create(ChannelCreate(id=channel_id, title=title, username=username, url=url), session)
    else:
        logger.info(f"Обновленны данные канала {channel.id}, {channel.username}")
        await ChannelService.update(channel.id, ChannelUpdate(id=channel_id, title=title, username=username, url=url), session)

    return await list_channels(CallbackQuery(data="channels",
                                             id=str(uuid.uuid4()),
                                             from_user=message.from_user,
                                             date=message.date, 
                                             chat_instance=str(message.chat.id), 
                                             message=message), state, session, bot)
