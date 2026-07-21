from datetime import datetime
from typing import Optional

from base import BaseJobModel, JobStatus, ModelType
from pydantic import BaseModel, Field, HttpUrl


class DemixResponse(BaseJobModel):
    """Response model for POST /demix"""

    message: str = Field(..., description="Separate message")
    status_url: HttpUrl = Field(..., description="URL to check job status")
    result_url: HttpUrl = Field(..., description="URL to download results")
    cancel_url: HttpUrl = Field(..., description="URL to cancel the job")


class JobResponse(BaseJobModel):
    """Response model for GET /demix/{id}"""

    status: JobStatus = Field(..., description="Current job status")
    progress: float = Field(
        default=0.0, ge=0, le=100, description="Progress percentage"
    )
    created_at: datetime = Field(..., description="When job was created")
    updated_at: datetime = Field(..., description="When job was last updated")
    model: ModelType = Field(..., description="Demucs model to use for separation")
    stems: Optional[list[str]] = Field(
        default=None, description="List of stem names when completed"
    )
    estimated_seconds_remaining: int = Field(
        description="Estimated seconds until completion (only when processing)"
    )
    size_bytes: int = Field(..., description="Input audio size in bytes")
    duration_seconds: float = Field(..., description="Input audio duration in seconds")
    sample_rate_hz: int = Field(..., description="Input audio sample rate in Hz")
    channels: int = Field(..., description="Input audio number of channels")
    expires_at: datetime = Field(..., description="When the result will be deleted")


class JobCancelResponse(BaseJobModel):
    """Response model for POST /demix/{id}/cancel"""

    message: str = Field(..., description="Canccel job message")
    status: str = Field(..., description="Current job status")


class JobListResponse(BaseModel):
    """Response model for GET /demix/all (admin only)"""

    jobs: list[JobResponse] = Field(..., description="List of jobs")
    total: int = Field(..., description="Total number of jobs")
    limit: int = Field(default=100, description="Number of jobs returned")
