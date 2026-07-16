import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4

from app.api.models.base import JobStatus, ModelType
from app.core.config import settings


@dataclass
class Job:
    """Entity for managing a track's demix process lifespan"""

    id: UUID
    status: JobStatus
    progress: float
    created_at: datetime
    updated_at: datetime
    model: ModelType

    stems: Optional[list[str]] = None
    estimated_seconds_remaining: Optional[int] = None
    sample_rate: Optional[int] = None
    duration_seconds: Optional[int] = None
    file_size_bytes: Optional[int] = None

    input_path: Optional[str] = None
    output_dir: Optional[str] = None
    expires_at: Optional[str] = None

    def to_response(self) -> dict[str, Any]:
        return {
            # todo
        }


class JobManager:
    def __init__(self):
        self._jobs: dict[UUID, Job] = {}
        self.storage_path = Path(settings.STORAGE_PATH)
        self._load_jobs()

    def create_job(self, model: ModelType) -> UUID:
        job = Job(
            id=uuid4(),
            status=JobStatus.PENDING,
            progress=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            model=model,
        )
        self._jobs[job.id] = job
        self._save_job_data(job)
        return job.id

    def _save_job_data(self, job: Job):
        track_dir = self.storage_path / str(job.id)
        track_dir.mkdir(exist_ok=True)

        job_data_path = track_dir / "job.json"
        with open(job_data_path, "w") as f:
            json.dump(asdict(job), f, indent=2)

    def _load_jobs(self) -> list[Job]: ...
