from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_DSN: RedisDsn

    POSTGRES_DSN: PostgresDsn
    REDIS_TIMEOUT: float = 0.5


settings = Settings()
