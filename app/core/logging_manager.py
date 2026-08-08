import logging
import re
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import structlog
from structlog.types import EventDict, Processor

from .config import settings


def _drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    event_dict.pop("color_message", None)
    return event_dict


def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class LoggingManager:
    def __init__(
        self,
        role: str,
        log_to_file: bool = False,
        log_format: str = "default",
        log_level: str = "INFO",
    ):
        self._configure_structlog(role, log_format, log_level)

    def _configure_structlog(self, role: str, log_format: str, log_level: str):
        timestamper = structlog.processors.TimeStamper(fmt="iso")

        shared_processors: list[Processor] = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.stdlib.ExtraAdder(),
            _drop_color_message_key,
            timestamper,
            structlog.processors.StackInfoRenderer(),
        ]

        if log_format == "json":
            shared_processors.append(structlog.processors.format_exc_info)

        structlog.configure(
            processors=shared_processors
            + [
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        log_renderer = (
            structlog.processors.JSONRenderer()
            if log_format == "json"
            else structlog.dev.ConsoleRenderer()
        )

        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                log_renderer,
            ],
        )

        root_logger = logging.getLogger()
        root_logger.setLevel(log_level.upper())

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        if settings.LOG_TO_FILE:
            log_path = Path(settings.LOGS_DIRECTORY) / f"{role}.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                filename=log_path,
                mode="a",
                maxBytes=settings.LOG_FILE_MAX_BYTES,
                backupCount=settings.LOG_FILE_BACKUP_COUNT,
                encoding="utf-8",
                delay=True,
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        logging.getLogger("uvicorn").handlers.clear()
        logging.getLogger("uvicorn.error").handlers.clear()
        logging.getLogger("uvicorn.access").handlers.clear()
        logging.getLogger("uvicorn").propagate = True
        logging.getLogger("uvicorn.error").propagate = True
        logging.getLogger("uvicorn.access").propagate = False

    @staticmethod
    def bind(*args, **new_values: Any):
        for arg in args:
            if hasattr(arg, "id"):
                key = _to_snake_case(type(arg).__name__)
                structlog.contextvars.bind_contextvars(**{key: arg.id})
        structlog.contextvars.bind_contextvars(**new_values)

    @staticmethod
    def unbind(*keys: str):
        structlog.contextvars.unbind_contextvars(*keys)

    @staticmethod
    def get_app_logger():
        return structlog.stdlib.get_logger(settings.APP_LOGGER_NAME)

    @staticmethod
    def get_access_logger():
        return structlog.stdlib.get_logger(settings.ACCESS_LOGGER_NAME)
