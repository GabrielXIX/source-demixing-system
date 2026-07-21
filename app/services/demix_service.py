from fastapi import BackgroundTasks, HTTPException
from storage_service import StorageService

from app.core.audio_processor import AudioProcessor
from app.core.demucs_engine import DemucsEngine
from app.core.job_manager import JobManager
from app.core.logger import logger


class DemixService:
    """Orchestrates the demix process"""

    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.demucs_engine = DemucsEngine()
        self.job_manager = JobManager()
        self.storage_service = StorageService()

    async def start_demix(self, data, background_tasks: BackgroundTasks):
        try:
            logger.info("Demix process started")
            file = data.file
            model = data.model

            file_metadata = self.audio_processor.validate_file(file)
            logger.info("File validated")

            job_id = self.job_manager.create_job(model)
            logger.info("Job created")
            logger.bind(job_id=job_id)

            input_path = await self.storage_service.save_input(
                job_id, file, file_metadata.extension
            )
            logger.info("File saved to storage")
            # todo: add method to ensure saved file integrity
            self.job_manager.update_job(job_id, input_path=input_path)

            track_metadata = self.audio_processor.validate_track(file)
            logger.info("Track validated")
            self.job_manager.update_job(
                job_id,
                duration_seconds=track_metadata.duration_seconds,
                sample_rate_hz=track_metadata.sample_rate_hz,
                channels=track_metadata.channels,
            )

            # 5. Save metadata
            # 5.1 Update job status

            # 6. Start background task (demucs engine, storage service, job manager)
            # 6.1 Update job status
            logger.info("Background demix process started")
            # 5. Return job id for added job

            logger.unbind("job_id")
            return job_id
        except Exception as e:
            # todo: do cleanup if try fails
            raise HTTPException(status_code=500, detail="error")
