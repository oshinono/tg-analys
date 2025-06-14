from aiogram.types import Message
from voice_to_text.utils import bynary_to_ogg
from voice_to_text.service import WhisperService
from typing import BinaryIO
from aiogram import Bot
from aiogram.fsm.context import FSMContext

async def audio_message_to_text(message: Message, bot: Bot) -> str:
    audio: BinaryIO = await bot.download(message.voice.file_id)
    ogg_audio = await bynary_to_ogg(audio)
    transcribe = await WhisperService.transcribe(ogg_audio)
    return transcribe

async def check_before_unuse_prompt(state: FSMContext) -> bool:
    prompt_id = await state.get_value('current_prompt_id')
    used_prompt_id = await state.get_value('used_prompt_id')
    if not prompt_id == used_prompt_id:
        return False
    return True

