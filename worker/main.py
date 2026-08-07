import dramatiq
from dramatiq.brokers.redis import RedisBroker

from app.core.config import settings
from app.core.demucs_engine import DemucsEngine
from app.core.job_manager import JobManager
from app.infrastructure.redis import create_broker_redis, create_sync_jobs_redis
from app.services.storage_service import StorageService
from worker.context import WorkerContext
from worker.demix_processor import DemixProcessor

broker_redis = create_broker_redis(settings)
broker = RedisBroker(client=broker_redis)
dramatiq.set_broker(broker)

jobs_redis = create_sync_jobs_redis(settings)

job_manager = JobManager(redis_client=jobs_redis, settings=settings)
storage_service = StorageService(settings=settings)
demucs_engine = DemucsEngine()

_context = WorkerContext(
    job_manager=job_manager,
    demix_processor=DemixProcessor(
        storage_service=storage_service, demucs_engine=demucs_engine
    ),
    logger="",
)


def get_context() -> WorkerContext:
    return _context


import worker.actors
