import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import SecretStr, RedisDsn, PostgresDsn


def get_project_root() -> Path:
    return Path(__file__).parent.parent


class BotConfig(BaseSettings):
    token: SecretStr
    channel_id: int

    redis_dsn: RedisDsn
    postgres_uri: PostgresDsn

    class Config:
        env_file = os.path.join(get_project_root(), '.env')
        env_file_encoding = 'utf-8'


bot_config = BotConfig()
