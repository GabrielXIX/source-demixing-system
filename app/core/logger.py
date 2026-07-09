import logging
import re
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Optional

import structlog
from structlog.types import EventDict, Processor

from .config import settings


def _drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    event_dict.pop("color_message", None)
    return event_dict


def _to_snake_case(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class Logger:
    _instance = None

    def __init__(self, json_logs: bool = False, log_level: str = "INFO"):
        if Logger._instance is None:
            self._configure_structlog(json_logs, log_level)
            Logger._instance = self

        self.logger = structlog.stdlib.get_logger(settings.APP_LOGGER_NAME)

    def _configure_structlog(self, json_logs: bool, log_level: str):
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

        if json_logs:
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
            if json_logs
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
            log_path = Path(settings.LOG_FILE_PATH)
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

    def bind(self, *args, **new_values: Any):
        for arg in args:
            if hasattr(arg, "id"):
                key = _to_snake_case(type(arg).__name__)
                structlog.contextvars.bind_contextvars(**{key: arg.id})
        structlog.contextvars.bind_contextvars(**new_values)

    @staticmethod
    def unbind(*keys: str):
        structlog.contextvars.unbind_contextvars(*keys)

    def debug(self, event: Optional[str] = None, *args: Any, **kwargs: Any):
        self.logger.debug(event, *args, **kwargs)

    def info(self, event: Optional[str] = None, *args: Any, **kwargs: Any):
        self.logger.info(event, *args, **kwargs)

    def warning(self, event: Optional[str] = None, *args: Any, **kwargs: Any):
        self.logger.warning(event, *args, **kwargs)

    def error(self, event: Optional[str] = None, *args: Any, **kwargs: Any):
        self.logger.error(event, *args, **kwargs)

    def critical(self, event: Optional[str] = None, *args: Any, **kwargs: Any):
        self.logger.critical(event, *args, **kwargs)

    def exception(self, event: Optional[str] = None, *args: Any, **kwargs: Any):
        self.logger.exception(event, *args, **kwargs)


logger = Logger(json_logs=settings.LOG_JSON_FORMAT, log_level=settings.LOG_LEVEL)
