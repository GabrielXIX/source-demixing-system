from enum import StrEnum


class LogFormat(StrEnum):
    DEFAULT = "default"
    JSON = "json"


class LogRole(StrEnum):
    API = "api"
    WORKER = "worker"
