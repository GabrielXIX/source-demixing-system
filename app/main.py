from api.routers.demix import router as demix_router
from fastapi import FastAPI

from app.core.config import settings
from app.core.enums import LogRole
from app.core.lifespan import lifespan
from app.core.logging_manager import LoggingManager

LoggingManager.initialize(role=LogRole.API, settings=settings)

app = FastAPI(
    title="Source Demixing System", version="", description="", lifespan=lifespan
)
app.include_router(demix_router, prefix="v1")
