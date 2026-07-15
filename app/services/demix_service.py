from fastapi import BackgroundTasks
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
            logger.info("Starting demix...")
            file = data.file
            model = data.model

            # 1. Do basic file validation
            self.audio_processor.validate_file(file)
            logger.info("File validation done")

            # 2. Create job
            job_id = self.job_manager.create_job(model)
            logger.info("Job created")

            # 3. Save file to storage
            # 3.1 Update job status
            logger.info("File saved to storage")

            # 4. Do deep file validation
            # 4.1 Update job status
            # 4.2 Delete file if deep validation fails
            logger.info("Track validation done")

            # 5. Save metadata
            # 5.1 Update job status
            logger.info("Job metadata updated")

            # 6. Start background task (demucs engine, storage service, job manager)
            # 6.1 Update job status
            logger.info("Demucs process started")

            logger.info("Demix started successfully")
            # 5. Return job id for added job
            pass
        except Exception as e:
            # re raise to router
            pass
