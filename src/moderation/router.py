from aiogram import Router, F, Bot
from roles.filters import AccessFilter
from roles.enums import Roles
from aiogram.types import CallbackQuery, Message
from moderation.states import ModerationStates
from aiogram.fsm.context import FSMContext
from moderation.keyboards import get_moderation_keyboard, get_unapproved_keyboards, get_unapproved_prompt_keyboard
from database import RedisClient
from prompts.models import Prompt
from prompts.schemas import UnapprovedPrompt, PromptCreate
from prompts.service import PromptService
from keyboards import get_simple_back_keyboard
from prompts.dependencies import audio_message_to_text
import uuid
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

router.message.filter(AccessFilter(Roles.ADMIN))
router.callback_query.filter(AccessFilter(Roles.ADMIN))

@router.callback_query(F.data == "moderate")
async def moderate(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(ModerationStates.index)

    message_to_edit_id = callback.message.message_id
    await state.update_data(message_to_edit_id=message_to_edit_id)

    await bot.edit_message_text(text="Вы в режиме модерации",
                                message_id=message_to_edit_id,
                                chat_id=callback.from_user.id,
                                reply_markup=await get_moderation_keyboard())

@router.callback_query(ModerationStates.unapproved_prompts, F.data == "back")
async def back(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await moderate(callback, state, bot)


@router.callback_query(ModerationStates.index, F.data == "unapproved_prompts")
async def unapproved_prompts(callback: CallbackQuery, state: FSMContext, redis: RedisClient, bot: Bot):
    await state.set_state(ModerationStates.unapproved_prompts)
    message_to_edit_id = await state.get_value('message_to_edit_id')
    if not message_to_edit_id:
        message_to_edit_id = callback.message.message_id
        await state.update_data(message_to_edit_id=message_to_edit_id)

    prompts = await redis.get_by_pattern("unapproved_prompt_*")
    validated_prompts = [Prompt(**UnapprovedPrompt(**prompt).model_dump(exclude={'creator_id'})) for prompt in prompts]

    await bot.edit_message_text(text="Непроверенные промпты: ",
                                message_id=message_to_edit_id,
                                chat_id=callback.from_user.id,
                                reply_markup=await get_unapproved_keyboards(validated_prompts, "prompt"))
    
@router.callback_query(ModerationStates.unapproved_prompt, F.data == "back")
async def back_from_prompt(callback: CallbackQuery, state: FSMContext, redis: RedisClient, bot: Bot):
    return await unapproved_prompts(callback, state, redis, bot)


@router.callback_query(ModerationStates.unapproved_prompts, F.data.startswith("prompt"))
async def prompt(callback: CallbackQuery, state: FSMContext, redis: RedisClient, bot: Bot):
    await state.set_state(ModerationStates.unapproved_prompt)

    message_to_edit_id = await state.get_value('message_to_edit_id')
    
    prompt_id = await state.get_value('unapproved_prompt_id')
    if not prompt_id:
        prompt_id = callback.data.split("_")[1]
        await state.update_data(unapproved_prompt_id=prompt_id)

    prompt = await redis.get(f"unapproved_prompt_{prompt_id}")
    

    await bot.edit_message_text(text=f"Промпт: <code>{prompt['text']}</code>",
                                message_id=message_to_edit_id,
                                chat_id=callback.from_user.id,
                                reply_markup=await get_unapproved_prompt_keyboard())
    
@router.callback_query(ModerationStates.unapproved_prompt, F.data == "approve_prompt")
async def approve_prompt(callback: CallbackQuery, state: FSMContext, session: AsyncSession, redis: RedisClient, bot: Bot):
    prompt_id = await state.get_value('unapproved_prompt_id')

    prompt = await redis.get(f"unapproved_prompt_{prompt_id}")
    creator_id = prompt["creator_id"]

    approved = await PromptService.create(PromptCreate(**prompt), session)

    await bot.send_message(chat_id=creator_id, text=f"Ваш промпт был одобрен модерацией ✅\n\n{approved.text}")
    
    await redis.delete(f"unapproved_prompt_{prompt_id}")
    await callback.answer(text="Вы одобрили промпт.", show_alert=True)

    return await unapproved_prompts(callback, state, redis, bot)

@router.callback_query(ModerationStates.want_to_reject, F.data == "back")
async def back_from_prompt_approving(callback: CallbackQuery, state: FSMContext, redis: RedisClient, bot: Bot):
    return await prompt(callback, state, redis, bot)

@router.callback_query(ModerationStates.unapproved_prompt, F.data == "reject_prompt")
async def reject_prompt(callback: CallbackQuery, state: FSMContext, redis: RedisClient, bot: Bot):
    await state.set_state(ModerationStates.want_to_reject)

    message_to_edit_id = await state.get_value('message_to_edit_id')
    await bot.edit_message_text(message_id=message_to_edit_id,
                                chat_id=callback.message.chat.id,
                                text="Объясните, почему вы хотите отклонить данный промпт: \n\nЭто можно сделать либо в виде голосового, либо в виде текста.",
                                reply_markup=await get_simple_back_keyboard())
    
@router.message(ModerationStates.want_to_reject)
async def prompt_rejected_with_message(message: Message, state: FSMContext, redis: RedisClient, bot: Bot):
    await message.delete()

    if message.voice:
        transcribe = await audio_message_to_text(message, bot)
    else:
        transcribe = message.text

    prompt_id = await state.get_value('unapproved_prompt_id')
    prompt = await redis.get(f"unapproved_prompt_{prompt_id}")

    await bot.send_message(chat_id=prompt["creator_id"], text=f"Ваш промпт был отклонен модерацией ❌\n\nПромпт: {prompt['text']}\n\nПравки: {transcribe}")

    await redis.delete(f"unapproved_prompt_{prompt_id}")

    return await unapproved_prompts(CallbackQuery(id=uuid.uuid4().hex,
                                           from_user=message.from_user,
                                           chat_instance=str(message.from_user.id)), 
                                           state, redis, bot)