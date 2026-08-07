from redis import Redis
from redis.asyncio import Redis as AsyncRedis

from app.core.config import Settings


def create_async_jobs_redis(settings: Settings) -> AsyncRedis:
    """
    Redis client for FastAPI.

    Used for:
    - API job queries
    - Creating jobs
    - Updating job state from HTTP handlers
    """
    return AsyncRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_JOBS_DB,
        decode_responses=True,
    )


def create_sync_jobs_redis(settings: Settings) -> Redis:
    """
    Redis client for worker processes.

    Used for:
    - JobManager
    - CleanupService
    - Worker-side job state updates
    """
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_JOBS_DB,
        decode_responses=True,
    )


def create_broker_redis(settings: Settings) -> Redis:
    """
    Redis client for Dramatiq broker.

    Used only by Dramatiq.
    """
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_BROKER_DB,
        decode_responses=True,
    )
