from loguru import logger
from sqlalchemy import TypeDecorator, DateTime
from datetime import datetime
from consts import CURRENT_TIMEZONE
import pytz

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