from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"]
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
