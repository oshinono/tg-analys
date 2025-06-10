from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str

    redis_password: str
    redis_port: str

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    our_channels_ids: list[int]
    superuser_tg_ids: list[int]

    google_table_channels_url: str
    google_table_users_url: str

    class Config:
        env_file = ".env"


settings = Settings()