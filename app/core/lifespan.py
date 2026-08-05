from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.audio_validator import AudioValidator
from app.core.config import settings
from app.core.job_manager import JobManager
from app.core.logger import logger
from app.infrastructure.redis import create_broker_redis, create_jobs_redis
from app.services.demix_service import DemixService
from app.services.storage_service import StorageService


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    # Do sanity check
    # Set timeout for startup operations

    # Connections
    jobs_redis = create_jobs_redis(settings)
    broker_redis = create_broker_redis(settings)

    # Infrastructure
    job_manager = JobManager(redis_client=jobs_redis, settings=settings)
    storage_service = StorageService(settings)
    audio_validator = AudioValidator()

    # Application service
    demix_service = DemixService(
        job_manager=job_manager,
        storage_service=storage_service,
        audio_validator=audio_validator,
        task_manager="",
    )

    app.state.demix_service = demix_service

    yield

    await jobs_redis.aclose()
    await broker_redis.aclose()

    logger.info("Application shutting down...")
