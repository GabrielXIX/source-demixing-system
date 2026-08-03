from pathlib import Path
from typing import Optional
from uuid import UUID

from redis import Redis
from rq import Queue

from app.api.models.base import JobStatus
from app.core.config import settings
from app.core.demucs_engine import DemucsEngine
from app.core.job_manager import JobManager
from app.core.logger import logger
from app.services.storage_service import StorageService


class TaskManager:
    def __init__(
        self,
        job_manager: Optional[JobManager] = None,
        storage_service: Optional[StorageService] = None,
        demucs_engine: Optional[DemucsEngine] = None,
        redis_client: Optional[Redis] = None,
    ):
        self._redis = redis_client or Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=1,
            decode_responses=True,
        )
        self._queue = Queue(
            settings.QUEUE_NAME,
            connection=self._redis,
            default_timeout=settings.JOB_TIMEOUT,
        )
        self._job_manager = job_manager or JobManager()
        self._storage_service = storage_service or StorageService()
        self._demucs_engine = demucs_engine or DemucsEngine()

    def enqueue_track_processing(self, job_id: UUID):
        logger.info("Track demix enqueue started")
        rq_job = self._queue.enqueue(
            self._process_track,
            job_id,
            result_ttl=86400,
            failure_ttl=86400,
            unique=True,
        )
        self._job_manager.sync_job(job_id, rq_job_id=rq_job.id, status=JobStatus.QUEUED)
        logger.info("Track demix enqueue completed")

    def _process_track(self, job_id: UUID):
        try:
            logger.info("Track demucs process started")
            # 1. Get job
            # job = self._job_manager.get_job(job_id)
            # if not job:
            #     logger.error(f"Job not found: {job_id}")
            #     return {"status": "failed", "error": "Job not found"}

            # # 2. Update status
            # self._job_manager.sync_job(job_id, status=JobStatus.PROCESSING, progress=10)

            # # 3. Get paths
            # input_path = Path(job.input_path)
            # output_dir = Path(settings.STORAGE_PATH) / str(job_id) / "output"
            # output_dir.mkdir(parents=True, exist_ok=True)

            # # 4. Process with Demucs
            # result = self._demucs_engine.process(
            #     input_path=input_path, output_dir=output_dir, model=job.model
            # )

            # # 5. Save stems
            # for stem_name, audio_data in result["stems"].items():
            #     self._storage_service.save_stem(job_id, stem_name, audio_data)

            # # 6. Create ZIP
            # zip_path = self._storage_service.create_zip(job_id)

            # # 7. Update job
            # self._job_manager.sync_job(
            #     job_id,
            #     status=JobStatus.COMPLETED,
            #     progress=100,
            #     stems=list(result["stems"].keys()),
            #     output_dir=str(output_dir),
            # )

            logger.info("Track demucs process completed")
        except Exception as e:
            logger.error(f"Processing failed: {job_id} - {e}")
            self._job_manager.sync_job(job_id, status=JobStatus.FAILED, error=str(e))
            raise
