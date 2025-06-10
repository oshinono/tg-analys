from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


default_bot_settings = DefaultBotProperties(parse_mode=ParseMode.HTML)
ALLOWED_UPDATES = ["message", "callback_query"]

import pytz
from sqlalchemy import text, types
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column


CURRENT_TIMEZONE = 'Europe/Moscow'

def get_updated_at_column() -> Mapped[datetime]:
    return mapped_column(
        types.DateTime(timezone=True),
        server_default=text(f"timezone('{CURRENT_TIMEZONE}', now())"),
        onupdate=lambda: datetime.now(pytz.timezone(CURRENT_TIMEZONE))
    )

def get_created_at_column() -> Mapped[datetime]:
    return mapped_column(
        types.DateTime(timezone=True),
        server_default=text(f"timezone('{CURRENT_TIMEZONE}', now())")
    )
