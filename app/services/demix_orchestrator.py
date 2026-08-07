from fastapi import HTTPException
from storage_service import StorageService

from app.core.audio_validator import AudioValidator
from app.core.job_manager import JobManager
from app.core.logger import logger
from app.infrastructure.demix_task_manager import DemixTaskManager


class DemixOrchestrator:
    """Orchestrates the demix process"""

    def __init__(
        self,
        job_manager: JobManager,
        storage_service: StorageService,
        audio_validator: AudioValidator,
        demix_task_manager: DemixTaskManager,
    ):
        self._job_manager = job_manager
        self._storage_service = storage_service
        self._audio_validator = audio_validator
        self._demix_task_manager = demix_task_manager

    async def start_demix(self, data):
        try:
            logger.info("Demix process started")
            file = data.file
            model = data.model

            file_metadata = self._audio_validator.validate_file(file)
            logger.info("File validated")

            job_id = self._job_manager.create_job()
            logger.info("Job created")
            logger.bind(job_id=job_id)
            self._job_manager.sync_job(
                job_id, model=model, size_bytes=file_metadata.size_bytes
            )

            input_path = await self._storage_service.save_input(
                job_id, file, file_metadata.extension
            )
            logger.info("File saved to storage")
            # todo: add method to ensure saved file integrity
            self._job_manager.sync_job(job_id, input_path=input_path)

            track_metadata = self._audio_validator.validate_track(file)
            logger.info("Track validated")
            self._job_manager.sync_job(
                job_id,
                duration_seconds=track_metadata.duration_seconds,
                sample_rate_hz=track_metadata.sample_rate_hz,
                channels=track_metadata.channels,
            )

            self._demix_task_manager.enqueue_demix(job_id)
            logger.info("Background demix process started")

            logger.unbind("job_id")
            return job_id
        except Exception as e:
            # todo: do cleanup if try fails
            raise HTTPException(status_code=500, detail="error")
