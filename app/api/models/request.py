from base import ModelType
from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class SeparateRequest(BaseModel):
    """Request model for POST /v1/separate"""

    file: UploadFile = File(...)
    model: ModelType = Field(
        default=ModelType.HTDEMUCS, description="Demucs model to use for separation"
    )
