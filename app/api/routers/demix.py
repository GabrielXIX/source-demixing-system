from uuid import UUID, uuid4

from fastapi import APIRouter, Form, status
from fastapi.responses import FileResponse
from pydantic import HttpUrl

from app.api.models.base import DemixResponseLinks
from app.api.models.request import DemixRequest
from app.api.models.response import DemixResponse, JobCancelResponse, JobResponse

router = APIRouter(prefix="demix", tags=["Demix"])

MAX_FILE_SIZE = 200 * 1024 * 1024  # 500 MB


@router.post("", response_model=DemixResponse, status_code=status.HTTP_202_ACCEPTED)
async def demix(data: DemixRequest = Form(..., media_type="multipart/form-data")):
    # job_id = job_manager.create_job(data) # create job manager instance on server startup

    # return DemixResponse(
    #     id=uuid4(),
    #     message="",
    #     estimated_seconds=0,
    #     links=DemixResponseLinks(
    #         status=HttpUrl(""),
    #         result=HttpUrl(""),
    #         cancel=HttpUrl("")
    #     )
    # )
    pass


@router.get("/{id}", response_model=JobResponse)
def get_job(id: UUID):
    """Get demix job"""
    # job = job_manager.get_job(id) # job already of type JobResponse

    # return job
    pass


@router.get("/{id}/result", response_class=FileResponse)
def get_job_result(id: UUID):
    """Download separated stems as ZIP file"""
    # job_result = job_manager.get_job_result(id)

    # return job_result
    pass


@router.delete(
    "/{id}/cancel",
    response_model=JobCancelResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_job(id: UUID):
    """Cancel a queued or processing job."""
    # response = job_manager.cancel_job(id)

    # return JobCancelResponse(
    #     id=uuid4(),
    #     message="response",
    #     status=""
    # )
    pass
