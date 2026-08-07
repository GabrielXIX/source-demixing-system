from app.core.job_manager import JobManager
from worker.demix_processor import DemixProcessor


class WorkerContext:
    def __init__(
        self,
        job_manager: JobManager,
        demix_processor: DemixProcessor,
        logger="",  # todo: Implement logger in worker
    ):
        self.job_manager = job_manager
        self.demix_processor = demix_processor
