from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_LOGGER_NAME: str = "sds.app_logs"
    ACCESS_LOGGER_NAME: str = "sds.access_logs"

    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = False
    LOG_INCLUDE_STACK: bool = False
    LOG_TO_FILE: bool = False
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_FILE_MAX_BYTES: int = 5 * 1024 * 1024  # 5 MB
    LOG_FILE_BACKUP_COUNT: int = 3

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
