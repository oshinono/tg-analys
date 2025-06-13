from aiogram import Router, F, Bot
from roles.filters import AccessFilter
from roles.enums import Roles
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from prompts.states import PromptStates
from keyboards import get_simple_back_keyboard
from prompts.dependencies import audio_message_to_text
from router import index_callback
from keyboards import get_objects_keyboards
from prompts.keyboards import get_confirm_prompt_keyboard
from database import RedisClient
from prompts.schemas import UnapprovedPrompt
from prompts.service import PromptService
from aiogram.filters import or_f

from config import settings
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()
router.callback_query.filter(AccessFilter(Roles.USER))
router.message.filter(AccessFilter(Roles.USER))

@router.callback_query(PromptStates.prompts, F.data == "back")
async def back_from_prompts(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await index_callback(callback, state)

@router.callback_query(F.data == "prompts")
async def prompts_callback(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.set_state(PromptStates.prompts)
    all_prompts = await PromptService.get_all(session, parent_guid=None)

    await callback.message.edit_text("Все промпты", reply_markup=await get_objects_keyboards(all_prompts, 'prompt'))

@router.callback_query(PromptStates.prompt_action, F.data == "back")
async def back_from_prompts(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await prompts_callback(callback, state, session)

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
                              parent_guid=await state.get_value("prompt_parent_guid"),
                              guid=str(uuid.uuid4()),
                              creator_id=callback.from_user.id)
    
    data = new_prompt.model_dump()

    await redis.set(f"unapproved_prompt_{data['guid']}", data, ttl=settings.unapproved_materials_ttl_hours * 60 * 60)

    await callback.answer(text="Промпт добавлен в очередь на модерацию", show_alert=True)
    return await prompts_callback(callback, state, session)