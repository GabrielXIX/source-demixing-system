from enum import Enum
from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class BaseJobModel(BaseModel):
    """Base model for job-related internal models"""

    id: UUID = Field(..., description="Unique Job Identifier")


class ModelType(str, Enum):
    """Enums for model types"""

    HTDEMUCS = "htdemucs"
    HTDEMUCS_FT = "htdemucs_ft"
    HTDEMUCS_6S = "htdemucs_6s"


class JobStatus(str, Enum):
    """Enums for job statuses"""

    PENDING = "pending"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
