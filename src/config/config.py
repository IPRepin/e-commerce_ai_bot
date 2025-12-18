from functools import lru_cache

from pydantic.v1 import BaseSettings
from pydantic_settings import SettingsConfigDict

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    # OPENROUTER
    OPENROUTER_API_KEY: str
    OPENROUTER_URL: str
    OPENROUTER_MODEL: str

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings: Settings = get_settings()