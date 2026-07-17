import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID


def json_encoder(obj: Any) -> str:
    if isinstance(obj, UUID):
        return str(obj)

    if isinstance(obj, datetime):
        return obj.isoformat()

    if isinstance(obj, Path):
        return str(obj)

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def write_json_file(data: Any, fp, **kwargs) -> None:
    json.dump(data, fp, default=json_encoder, **kwargs)


def to_json_string(data: Any, **kwargs) -> str:
    return json.dumps(data, default=json_encoder, **kwargs)
