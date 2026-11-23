from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    core_api_token: SecretStr = Field(
        default=SecretStr(""),
        validation_alias="MOHSEN_API_TOKEN",
    )
    core_url: str = Field(
        default="http://127.0.0.1:8765",
        validation_alias="MOHSEN_CORE_URL",
    )


settings = Settings()
