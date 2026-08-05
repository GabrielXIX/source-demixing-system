from redis.asyncio import Redis

from app.core.config import Settings


def create_jobs_redis(settings: Settings) -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.JOBS_REDIS_DB,
        decode_responses=True,
    )


def create_broker_redis(settings: Settings) -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.BROKER_REDIS_DB,
        decode_responses=True,
    )
