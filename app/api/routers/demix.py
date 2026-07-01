from uuid import UUID

from fastapi import APIRouter, Form, status
from fastapi.responses import FileResponse

from app.api.models.request import DemixRequest
from app.api.models.response import DemixResponse, JobCancelResponse, JobResponse

router = APIRouter(prefix="demix", tags=["Demix"])

MAX_FILE_SIZE = 200 * 1024 * 1024  # 500 MB


@router.post("", response_model=DemixResponse, status_code=status.HTTP_202_ACCEPTED)
async def demix(data: DemixRequest = Form(..., media_type="multipart/form-data")):
    # Create Job
    # Return Job ID
    pass


@router.get("/{id}", response_model=JobResponse)
def get_job(id: UUID):
    """Get demix job"""
    pass


@router.get("/{id}/result", response_class=FileResponse)
def get_job_result(id: UUID):
    """Download separated stems as ZIP file"""
    pass


@router.delete(
    "/{id}/cancel",
    response_model=JobCancelResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_job(id: UUID):
    """Cancel a queued or processing job."""
    pass
