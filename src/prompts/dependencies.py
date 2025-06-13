from aiogram.types import Message
from voice_to_text.utils import bynary_to_ogg
from voice_to_text.service import WhisperService
from typing import BinaryIO
from aiogram import Bot

async def audio_message_to_text(message: Message, bot: Bot) -> str:
    audio: BinaryIO = await bot.download(message.voice.file_id)
    ogg_audio = await bynary_to_ogg(audio)
    transcribe = await WhisperService.transcribe(ogg_audio)
    return transcribe