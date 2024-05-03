from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator, Field
from typing import Any, Annotated
from email_validator import validate_email

Port = Annotated[int, Field(ge=0, le=65535)]


def normalize_none(env_value: str) -> Any | None:
    if env_value == "":
        return None
    return env_value


class SMTPSettings(BaseSettings):
    server: str
    port: Port
    user: str
    password: SecretStr

    normalize_none = field_validator("*", mode="before")(normalize_none)

    @field_validator("user", mode="before")
    def validate_email(cls, v):
        valid = validate_email(v)
        return valid.email


class Settings(BaseSettings):
    smtp: SMTPSettings
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        arbitrary_types_allowed=True,
        env_nested_delimiter="__",
    )


settings = Settings()