from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MOHSEN_ADMIN_", extra="ignore")

    admin_token: SecretStr = SecretStr("")
    core_url: str = "http://127.0.0.1:8765"


settings = Settings()
