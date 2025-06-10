from parser import BaseGTParser
from channels.models import Channel


class ChannelsParser(BaseGTParser):

    """
    -----------------------------------
    channel_id | title | username | url
    -----------------------------------
    """

    async def parse(self) -> list[Channel]:
        data = await self._parse_all_rows(worksheets=[0])
        channels = []

        channels_worksheet = data[0]
        for row in channels_worksheet:
            channel = Channel(
                id=row[0],
                title=row[1],
                username=row[2],
                url=row[3]
            )
            channels.append(channel)
        return channels