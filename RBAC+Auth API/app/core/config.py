#/core/config.py
#configuration file

from pydantic_settings import BaseSettings #helps read env vars into a class

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

#create single importable setting instance
settings = Settings()