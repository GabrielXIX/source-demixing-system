from api.routers.demix import router as demix_router
from fastapi import FastAPI

from app.core.lifespan import lifespan

app = FastAPI(
    title="Source Demixing System", version="", description="", lifespan=lifespan
)
app.include_router(demix_router, prefix="v1")
