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

            # 1. Do basic file validation
            file_metadata = self.audio_processor.validate_file(file)
            logger.info("File validated")

            # 2. Create job
            job_id = self.job_manager.create_job(model)
            logger.info("Job created")
            logger.bind(job_id=job_id)

            # 3. Save file to storage
            # 3.1 Update job status
            input_path = await self.storage_service.save_input(
                job_id, file, file_metadata.extension
            )
            logger.info("File saved to storage")
            # Update job's input path

            # 4. Do deep file validation
            # 4.1 Update job status
            # 4.2 Delete file if deep validation fails
            logger.info("Track validated")

            # 5. Save metadata
            # 5.1 Update job status

            # 6. Start background task (demucs engine, storage service, job manager)
            # 6.1 Update job status
            logger.info("Background demix process started")
            # 5. Return job id for added job

            logger.unbind("job_id")
            return job_id
        except Exception as e:
            raise HTTPException(status_code=500, detail="error")
