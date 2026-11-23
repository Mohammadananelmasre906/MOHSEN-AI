from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    admin_token: SecretStr = Field(
        default=SecretStr(""),
        validation_alias="MOHSEN_ADMIN_TOKEN",
    )
    core_url: str = Field(
        default="http://127.0.0.1:8765",
        validation_alias="MOHSEN_CORE_URL",
    )


settings = Settings()
