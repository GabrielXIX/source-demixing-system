from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_VERSION: str = "v1"
    API_BASE_URL: str = "http://localhost:8000"

    APP_LOGGER_NAME: str = "sds.app_logs"
    ACCESS_LOGGER_NAME: str = "sds.access_logs"

    LOG_LEVEL: str = "INFO"
    LOG_JSON_FORMAT: bool = False
    LOG_INCLUDE_STACK: bool = False
    LOG_TO_FILE: bool = False
    LOGS_DIRECTORY: str = "logs/"
    LOG_FILE_MAX_BYTES: int = 5 * 1024 * 1024  # 5 MB
    LOG_FILE_BACKUP_COUNT: int = 3

    STORAGE_PATH = "storage"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_JOBS_DB = 0
    REDIS_BROKER_DB = 1
    QUEUE_NAME: str = "demix-queue"
    JOB_TIMEOUT: int = 600

    JOB_RESULT_RETENTION_SECONDS = 60 * 60 * 24  # 1 day

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
