from base import ModelType
from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class DemixRequest(BaseModel):
    """Request model for POST /demix"""

    file: UploadFile = File(...)
    model: ModelType = Field(
        default=ModelType.HTDEMUCS, description="Demucs model to use for separation"
    )
