from uuid import UUID

from deps import get_demix_service
from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import FileResponse

from app.api.models.request import DemixRequest
from app.api.models.response import DemixResponse, JobCancelResponse, JobResponse
from app.api.utils.links import build_demix_response_urls
from app.services.demix_service import DemixService

router = APIRouter(prefix="demix", tags=["Demix"])


@router.post("", response_model=DemixResponse, status_code=status.HTTP_202_ACCEPTED)
async def demix(
    data: DemixRequest = Form(..., media_type="multipart/form-data"),
    demix_service: DemixService = Depends(get_demix_service),
):
    job_id = await demix_service.start_demix(data)
    status_url, result_url, cancel_url = build_demix_response_urls(job_id)

    return DemixResponse(
        id=job_id,
        message="Demix process started successfully",
        status_url=status_url,
        result_url=result_url,
        cancel_url=cancel_url,
    )


@router.get("/{id}", response_model=JobResponse)
def get_job(id: UUID):
    """Get demix job"""
    # job = demix_service.get_demix_status(id) # job already of type JobResponse

    # return job
    pass


@router.get("/{id}/result", response_class=FileResponse)
def get_job_result(id: UUID):
    """Download separated stems as ZIP file"""
    # job_result = demix_service.get_demix_result(id)

    # return job_result
    pass


@router.delete(
    "/{id}/cancel",
    response_model=JobCancelResponse,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_job(id: UUID):
    """Cancel a queued or processing job."""
    # response = job_manager.cancel_demix(id)

    # return JobCancelResponse(
    #     id=uuid4(),
    #     message="response",
    #     status=""
    # )
    pass
