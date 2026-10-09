from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    redis_host: str
    redis_port: int
    redis_db: str
    cache_ttl_seconds: int
    cache_exercises_key: str
    cache_workouts_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    @property
    def database_url(self):
        return URL.create(
            drivername="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db
        )

    @property
    def redis_url(self):
        return (
            f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
        )

settings = Settings()
