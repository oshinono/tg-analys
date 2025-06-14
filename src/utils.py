from loguru import logger
from sqlalchemy import TypeDecorator, DateTime
from datetime import datetime
from consts import CURRENT_TIMEZONE
import pytz
from aiogram.fsm.context import FSMContext

def setup_logger():
    logger.add('logs/bot.log',
               format="{time} {level} {message}",
               level="DEBUG", 
               rotation='10 MB',
               colorize=True,
               compression='zip')


class TimestampType(TypeDecorator):
    impl = DateTime

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return datetime.fromtimestamp(value, pytz.timezone(CURRENT_TIMEZONE))
        return value
    
async def clear_state(state: FSMContext):
    used_prompt_id = await state.get_value('used_prompt_id')
    await state.clear()
    if used_prompt_id:
        await state.update_data(used_prompt_id=used_prompt_id)