"""Environment-based configuration (Pydantic Settings)."""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    interfaze_api_key: str = Field(default="")
    sarvam_api_key: str = Field(default="")

    provider_ocr: str = Field(default="fake")
    provider_llm: str = Field(default="fake")
    provider_tts: str = Field(default="fake")

    delete_uploads_after: str = Field(default="processing")
    log_personal_data: bool = Field(default=False)

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    log_level: str = Field(default="INFO")

    app_name: str = "Satbara Saathi"
    app_version: str = "0.1.0"
    consent_required: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
