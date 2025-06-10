from repository import BaseRepository
from channels.models import Channel

class ChannelRepository(BaseRepository):
    model = Channel
