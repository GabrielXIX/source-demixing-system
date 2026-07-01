from api.routers.demix import router as demix_router
from fastapi import FastAPI

app = FastAPI(title="Source Demixing System", version="", description="")

app.include_router(demix_router, prefix="v1")
