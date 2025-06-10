from pydantic import BaseModel

class ChannelCreate(BaseModel):
    id: int
    title: str
    username: str
    url: str

class ChannelUpdate(BaseModel):
    title: str | None = None
    username: str | None = None
    url: str | None = None