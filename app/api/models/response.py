from datetime import datetime
from typing import Optional

from base import BaseJobModel, DemixResponseLinks, JobStatus, ModelType
from pydantic import BaseModel, Field


class DemixResponse(BaseJobModel):
    """Response model for POST /demix"""

    message: str = Field(..., description="Separate message")
    estimated_seconds: int = Field(..., description="Estimated seconds for processing")
    links: DemixResponseLinks = Field(
        ..., description="Links for status, result and cancellation"
    )


class JobResponse(BaseJobModel):
    """Response model for GET /jobs/{job_id}"""

    status: JobStatus = Field(..., description="Current job status")
    progress: float = Field(
        default=0.0, ge=0, le=100, description="Progress percentage"
    )
    created_at: datetime = Field(..., description="When job was created")
    updated_at: datetime = Field(..., description="When job was last updated")
    estimated_seconds_remaining: int = Field(
        description="Estimated seconds until completion (only when processing)"
    )
    stems: Optional[list[str]] = Field(
        default=None, description="List of stem names when completed"
    )
    model: ModelType = Field(..., description="Demucs model to use for separation")


class JobResultMetadata(BaseJobModel):
    """Response model for GET /jobs/{job_id}/result/metadata"""

    stems: list[str] = Field(..., description="List of stem names available")
    sample_rate: int = Field(..., description="Sample rate of stems in Hz")
    duration_seconds: float = Field(..., description="Duration of original audio")
    file_size_bytes: int = Field(..., description="Size of ZIP file in bytes")
    expires_at: datetime = Field(..., description="When the result will be deleted")


class JobCancelResponse(BaseJobModel):
    """Response model for POST /jobs/{job_id}/cancel"""

    message: str = Field(..., description="Canccel job message")
    status: str = Field(..., description="Current job status")


class JobListResponse(BaseModel):
    """Response model for GET /jobs (admin only)"""

    jobs: list[JobResponse] = Field(..., description="List of jobs")
    total: int = Field(..., description="Total number of jobs")
    limit: int = Field(default=100, description="Number of jobs returned")
