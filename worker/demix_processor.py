from app.core.demucs_engine import DemucsEngine
from app.core.job_manager import Job
from app.services.storage_service import StorageService


class DemixProcessor:
    def __init__(
        self,
        storage_service: StorageService,
        demucs_engine: DemucsEngine,
    ):
        self.storage_service = storage_service
        self.demucs_engine = demucs_engine

    def process(self, job: Job):
        ...
        # todo: processing logic
