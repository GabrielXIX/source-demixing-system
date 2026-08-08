import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, ClassVar, Optional
from uuid import UUID, uuid4

from redis.asyncio import Redis

from app.api.models.base import JobStatus, ModelType
from app.core.config import Settings
from app.core.exceptions import JobNotFoundError
from app.core.logging_manager import LoggingManager

log = LoggingManager.get_app_logger()


@dataclass
class Job:
    id: UUID
    status: JobStatus
    progress: float
    created_at: datetime

    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    model: Optional[ModelType] = None
    stems: Optional[list[str]] = None
    estimated_seconds_remaining: Optional[int] = None
    duration_seconds: Optional[int] = None
    sample_rate_hz: Optional[int] = None
    size_bytes: Optional[int] = None
    channels: Optional[int] = None
    input_path: Optional[str] = None
    output_dir: Optional[str] = None
    rq_job_id: Optional[UUID] = None

    @classmethod
    def from_redis(cls, data: dict[str, str]):
        return cls(
            id=UUID(data["id"]),
            status=JobStatus(data["status"]),
            progress=float(data["progress"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
            if data.get("updated_at")
            else None,
            expires_at=datetime.fromisoformat(data["expires_at"])
            if data.get("expires_at")
            else None,
            model=ModelType(data["model"]) if data.get("model") else None,
            stems=json.loads(data["stems"]) if data.get("stems") else None,
            estimated_seconds_remaining=int(data["estimated_seconds_remaining"])
            if data.get("estimated_seconds_remaining")
            else None,
            duration_seconds=int(data["duration_seconds"])
            if data.get("duration_seconds")
            else None,
            sample_rate_hz=int(data["sample_rate_hz"])
            if data.get("sample_rate_hz")
            else None,
            size_bytes=int(data["size_bytes"]) if data.get("size_bytes") else None,
            channels=int(data["channels"]) if data.get("channels") else None,
            input_path=data["input_path"] if data.get("input_path") else None,
            output_dir=data["output_dir"] if data.get("output_dir") else None,
            rq_job_id=UUID(data["rq_job_id"]) if data.get("rq_job_id") else None,
        )

    def to_response(self) -> dict[str, Any]:
        return {
            # todo
        }


class JobManager:
    """Entity for managing all demix processes in Redis"""

    _JOB_FIELDS: ClassVar[set[str]] = set(Job.__dataclass_fields__.keys())

    def __init__(self, redis_client: Redis, settings: Settings):
        self.redis = redis_client
        self.ttl_seconds = settings.JOB_RESULT_RETENTION_SECONDS
        self.storage_path = Path(settings.STORAGE_PATH)

        logger.info(
            "JobManager initialized",
            extra={
                "redis_db": self.redis,
                "ttl_seconds": self.ttl_seconds,
            },
        )

    def create_job(self) -> UUID:
        logger.debug("Job creation started")
        job = Job(
            id=uuid4(),
            status=JobStatus.PENDING,
            progress=0.0,
            created_at=datetime.now(),
        )
        track_dir = self.storage_path / str(job.id)
        track_dir.mkdir()

        self.sync_job(job.id, **asdict(job))

        logger.debug("Job creation completed")
        return job.id

    def get_job(self, job_id):
        logger.debug("Job retrieval started")
        key = str(job_id)
        data = self.redis.hgetall(key)

        if not data:
            raise JobNotFoundError("Job not found in Redis")

        job = Job.from_redis(data)  # type: ignore
        logger.debug("Job retrieval completed")
        return job

    def sync_job(self, job_id: UUID, **kwargs):
        logger.debug("Job sync started")
        key = str(job_id)
        parsed_data = self._get_parsed_dict(**kwargs)

        if "updated_at" not in parsed_data:
            parsed_data["updated_at"] = datetime.now().isoformat()
        if "expires_at" not in parsed_data:
            expires_at = datetime.now() + timedelta(seconds=self.ttl_seconds)
            parsed_data["expired_at"] = expires_at.isoformat()

        self.redis.hset(key, mapping=parsed_data)
        self.redis.expire(key, self.ttl_seconds)
        logger.debug("Job sync completed")

    def _get_parsed_dict(self, **kwargs):
        logger.debug("Keyword arguments parse started")
        valid_fields = self._JOB_FIELDS
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}

        unknown = set(kwargs.keys()) - valid_fields
        if unknown:
            logger.warning(f"Unknown fields ignored: {unknown}")

        parsed_dict = {}
        for k, v in filtered_kwargs.items():
            if v is None:  # log this
                continue
            elif isinstance(v, (UUID, Path, int, float)):
                parsed_dict[k] = str(v)
            elif isinstance(v, datetime):
                parsed_dict[k] = v.isoformat()
            elif isinstance(v, list):
                parsed_dict[k] = json.dumps(v)
            else:
                parsed_dict[k] = str(v)
        logger.debug("Keyword arguments parse completed")
        return parsed_dict

    def get_all_jobs(self): ...
