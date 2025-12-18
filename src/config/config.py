from functools import lru_cache

from pydantic.v1 import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class DataSettings(BaseSettings):
    FAQ_PATH: str = "data/faq.json"
    ORDERS_PATH: str = "data/orders.json"


class ShopSettings(BaseSettings):
    BRAND_NAME: str = "Shoply"


class LoggingSettings(BaseSettings):
    LOGGER_LEVEL: str = "INFO"
    LOGS_DIR: str = "logs"


class OpenrouterSettings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_URL: str
    OPENROUTER_MODEL: str


class Settings(BaseSettings):
    data: DataSettings = DataSettings()
    shop: ShopSettings = ShopSettings()
    logging: LoggingSettings = LoggingSettings()
    openrouter: OpenrouterSettings = OpenrouterSettings()


    class Config:
        env_file = ".env"
        env_ignore_empty = True
        extra = "ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings: Settings = get_settings()