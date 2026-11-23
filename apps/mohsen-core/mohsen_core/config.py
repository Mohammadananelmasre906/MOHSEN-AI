from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MOHSEN_", extra="ignore")

    core_api_token: SecretStr = SecretStr("")
    app_name: str = "MOHSEN CORE"
    version: str = "0.1.0"


settings = Settings()
