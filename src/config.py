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

    admin_permission_level: int # 4
    smm_permission_level: int # 4
    user_permission_level: int # 1
    superuser_permission_level: int # 999

    google_table_channels_url: str
    google_table_users_url: str

    hugging_face_api_key: str

    unapproved_materials_ttl_hours: int

    class Config:
        env_file = ".env"


settings = Settings()