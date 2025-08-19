from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict, BaseSettings
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: SecretStr
    POSTGRES_DB: SecretStr


    @property
    def POSTGRES_URL(self) -> str:
        return(
            f"postgresql+asyncpg://{self.POSTGRES_USER.get_secret_value()}:"
            f"{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRES_HOST.get_secret_value()}/{self.POSTGRES_DB.get_secret_value()}"
        )

    model_config = SettingsConfigDict(
        env_file=BASE_PATH/".env",
        env_file_encoding="utf-8"
        )


settings = Settings()
