from typing import Dict, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_SCHEMA: str = ""
    ALLOWED_HOSTS: list = ["*"]
    DATABASE_ECHO: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    REFRESH_TOKEN_ACTIVE: bool = True
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7    

    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_file_encoding="utf-8", # UTF-8 support
        extra="ignore"             # Ignore undefined environment variables
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.validate_settings()

    def validate_settings(self) -> None:
        missing_vars = []
        if not self.DATABASE_URL:
            missing_vars.append("DATABASE_URL")

settings = Settings()