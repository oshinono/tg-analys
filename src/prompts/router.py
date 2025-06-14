from aiogram import Router, F, Bot
from roles.filters import AccessFilter
from roles.enums import Roles
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from prompts.states import PromptStates
from keyboards import get_simple_back_keyboard
from prompts.dependencies import audio_message_to_text, check_before_unuse_prompt
from router import index_callback
from keyboards import get_objects_keyboards
from prompts.keyboards import get_confirm_prompt_keyboard, get_prompt_keyboard
from database import RedisClient
from prompts.schemas import UnapprovedPrompt
from prompts.service import PromptService
from aiogram.filters import or_f
from prompts.models import Prompt
from config import settings
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from consts import DATETIME_PATTERN
from loguru import logger
from utils import clear_state


router = Router()
router.callback_query.filter(AccessFilter(Roles.USER))
router.message.filter(AccessFilter(Roles.USER))

@router.callback_query(PromptStates.prompts, F.data == "back")
async def back_from_prompts(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await index_callback(callback, state)

@router.callback_query(F.data == "prompts")
async def prompts_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await clear_state(state)
    await state.set_state(PromptStates.prompts)
    await state.update_data(message_to_edit_id=callback.message.message_id)

    all_prompts = await PromptService.get_all(session, parent_id=None)

    await callback.message.edit_text("Все промпты", reply_markup=await get_objects_keyboards(all_prompts, 'prompt'))

@router.callback_query(or_f(PromptStates.prompt_action, PromptStates.prompt), F.data == "back")
async def back_from_prompts(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await prompts_callback(callback, state, session)

@router.callback_query(PromptStates.prompts, F.data.startswith("prompt_"))
async def prompt(callback: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    await state.set_state(PromptStates.prompt)
    message_to_edit_id = await state.get_value('message_to_edit_id')

    prompt_id = await state.get_value('current_prompt_id')
    if not prompt_id:
        prompt_id = callback.data.split("_")[1]
        await state.update_data(current_prompt_id=prompt_id)

    used_prompt_id = await state.get_value('used_prompt_id')
    
    prompt: Prompt = await PromptService.get_by_id(prompt_id, session)

    text = f"Текст: {prompt.text}\n\n"
    text += f"Одобрен: {prompt.created_at}\n"
    text += f"Обновлен: {prompt.updated_at}"

    await bot.edit_message_text(text=text,
                                message_id=message_to_edit_id,
                                chat_id=callback.message.chat.id,
                                reply_markup=await get_prompt_keyboard(prompt_id == used_prompt_id))


@router.callback_query(PromptStates.prompt, F.data == "use_prompt")
async def use_this_prompt(callback: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    message_to_edit_id = await state.get_value('message_to_edit_id')
    prompt_id = await state.get_value('current_prompt_id')
    await state.update_data(used_prompt_id=prompt_id)
    return await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                               message_id=message_to_edit_id,
                                               reply_markup=await get_prompt_keyboard(True))

@router.callback_query(PromptStates.prompt, F.data == "deactivate_prompt")
async def use_this_prompt(callback: CallbackQuery, session: AsyncSession, bot: Bot, state: FSMContext):
    if not await check_before_unuse_prompt(state):
        return
    
    message_to_edit_id = await state.get_value('message_to_edit_id')
    await state.update_data(used_prompt_id=None)
    return await bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                               message_id=message_to_edit_id,
                                               reply_markup=await get_prompt_keyboard(False))

@router.callback_query(PromptStates.prompts, F.data == "add_new_prompt")
async def prompts(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(PromptStates.prompt_action)
    await state.update_data(message_to_edit_id=callback.message.message_id)
    await callback.message.edit_text("Напишите новый промпт\nили\nЗапишите голосовое с промптом", reply_markup=await get_simple_back_keyboard())

@router.message(PromptStates.prompt_action)
async def new_prompt(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(PromptStates.prompt_action)
    await message.delete()

    message_to_edit_id = await state.get_value("message_to_edit_id")

    if message.voice:
        transcribe = await audio_message_to_text(message, bot)
    else:
        transcribe = message.text

    text = f"Текст промпта: {transcribe}\n\nЕсли все хорошо, нажмите на кнопку ниже\nЕсли нет, то повторите свои действия"

    await state.update_data(prompt=transcribe)

    await bot.edit_message_text(text=text, 
                                chat_id=message.chat.id, 
                                message_id=message_to_edit_id,
                                reply_markup=await get_confirm_prompt_keyboard())

@router.callback_query(PromptStates.prompt_action, F.data == "confirm_prompt")
async def confirm_prompt(callback: CallbackQuery, state: FSMContext, redis: RedisClient, session: AsyncSession):
    new_prompt = UnapprovedPrompt(text=await state.get_value("prompt"), 
                              parent_id=await state.get_value("prompt_parent_id"),
                              id=str(uuid.uuid4()),
                              creator_id=callback.from_user.id)
    
    data = new_prompt.model_dump()

    await redis.set(f"unapproved_prompt_{data['id']}", data, ttl=settings.unapproved_materials_ttl_hours * 60 * 60)

    await callback.answer(text="Промпт добавлен в очередь на модерацию", show_alert=True)
    return await prompts_callback(callback, state, session)