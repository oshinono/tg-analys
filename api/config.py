from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    tg_api_hash: str
    tg_api_id: str
    tg_phone: str
    tg_password: str