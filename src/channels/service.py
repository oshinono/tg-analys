from service import BaseService
from channels.models import Channel
from channels.parser import ChannelsParser
from channels.repository import ChannelRepository
from config import settings
from oauth.google import agcm
from channels.schemas import ChannelCreate
from sqlalchemy.ext.asyncio import AsyncSession

class ChannelsService(BaseService):
    repository = ChannelRepository

    @classmethod
    async def parse_all_channels(cls) -> list[Channel]:
        parser = ChannelsParser(table_url=settings.channels_table_url, agcm=agcm)
        return await parser.parse()
    
    @classmethod
    async def load_all_channels(cls, session: AsyncSession) -> list[Channel]:
        channels = await cls.parse_all_channels()
        return await cls.repository.create_all([ChannelCreate(channel.id, channel.title, channel.username, channel.url) for channel in channels], session)