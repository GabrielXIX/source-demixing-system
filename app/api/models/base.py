from enum import Enum
from typing import TypedDict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, HttpUrl


class BaseJobModel(BaseModel):
    """Base model for job-related internal models"""

    id: UUID = Field(default_factory=uuid4, description="Unique Job Identifier")


class ModelType(str, Enum):
    """Enums for model types"""

    HTDEMUCS = "htdemucs"
    HTDEMUCS_FT = "htdemucs_ft"
    HTDEMUCS_6S = "htdemucs_6s"


class JobStatus(str, Enum):
    """Enums for job statuses"""

    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"


class DemixResponseLinks(TypedDict):
    """Response links for /demix"""

    status: HttpUrl
    result: HttpUrl
    result_metadata: HttpUrl
    cancel: HttpUrl
