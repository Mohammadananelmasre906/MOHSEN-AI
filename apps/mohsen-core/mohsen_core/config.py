from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    core_api_token: SecretStr = Field(
        default=SecretStr(""),
        validation_alias="MOHSEN_API_TOKEN",
    )
    app_name: str = "MOHSEN CORE"
    version: str = "0.1.0"


settings = Settings()
