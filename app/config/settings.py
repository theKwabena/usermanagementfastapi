import os
import secrets
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional, Any, Dict, Union
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator, FieldValidationInfo, EmailStr


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    REFRESH_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 12  # 12 days
    # PROJECT_NAME: str
    FIRST_ADMIN : EmailStr
    FIRST_ADMIN_PASSWORD : str
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQL_ALCHEMY_DATABASE_URI: Any

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before", check_fields=False)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    app_settings = Settings()
    return app_settings


settings = get_settings()
