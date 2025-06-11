from service import BaseService
from channels.models import Channel
from channels.parser import ChannelsParser
from channels.repository import ChannelRepository
from config import settings
from oauth.google import agcm
from channels.schemas import ChannelCreate, ChannelUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

class ChannelService(BaseService):
    repository = ChannelRepository

    @classmethod
    async def parse_all_channels(cls) -> list[Channel]:
        parser = ChannelsParser(table_url=settings.google_table_channels_url, agcm=agcm)
        return await parser.parse()
    
    @classmethod
    async def load_all_channels(cls, session: AsyncSession) -> list[Channel]:
        channels = await cls.parse_all_channels()
        created_channels = []
        updated_channels = []
        
        for channel in channels:
            existing_channel = await cls.repository.get_one_or_none(session=session, id=channel.id, username=channel.username)
            if existing_channel:
                channel_data = ChannelUpdate(
                    id=channel.id,
                    title=channel.title,
                    username=channel.username,
                    url=channel.url
                )
                updated_channel = await cls.repository.update(existing_channel.id, channel_data, session)
                updated_channels.append(updated_channel)
            else:
                new_channel = await cls.repository.create(
                    ChannelCreate(
                        id=channel.id,
                        title=channel.title,
                        username=channel.username,
                        url=channel.url
                    ),
                    session
                )
                created_channels.append(new_channel)
        
        return created_channels, updated_channels