from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    core_api_token: SecretStr = Field(
        default=SecretStr(""),
        validation_alias="MOHSEN_API_TOKEN",
    )
    database_path: str = Field(
        default=str(Path.home() / ".mohsen" / "data" / "mohsen.sqlite3"),
        validation_alias="MOHSEN_DATABASE_PATH",
    )
    app_name: str = "MOHSEN CORE"
    version: str = "0.2.0"


settings = Settings()
