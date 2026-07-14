from contextlib import asynccontextmanager

from api.routers.demix import router as demix_router
from fastapi import FastAPI

from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    # Read settings
    # Do sanity check
    # Set timeout for startup operations
    try:
        yield
    finally:
        # set timeout for shutdown operations
        logger.info("Application shutting down...")


app = FastAPI(
    title="Source Demixing System", version="", description="", lifespan=lifespan
)
app.include_router(demix_router, prefix="v1")
