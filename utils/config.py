from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

BASE_DIR = Path(__file__).resolve().parent.parent


class ModeType(str, Enum):
    dev = "dev"
    prod = "prod"


class JwtSettings(BaseModel):
    public_key: Path = BASE_DIR / "data" / "jwt-public.pem"
    private_key: Path = BASE_DIR / "data" / "jwt-private.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60


class Config(BaseSettings):
    APP_MODE: ModeType

    APP_ADMIN_USERNAME: str
    APP_ADMIN_PASSWORD: str

    APP_TG_CHAT_ID: str
    APP_TG_BOT_TOKEN: str

    JWT: JwtSettings = JwtSettings()

    @property
    def connection_string_async(self):
        return f"sqlite+aiosqlite:///{str(Path(__file__).resolve().parent.parent / 'data' / 'sqlite')}.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
