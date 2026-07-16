from uuid import UUID

from pydantic import HttpUrl

from app.core.config import settings


def build_demix_response_urls(job_id: UUID):
    return (
        HttpUrl(f"{settings.API_BASE_URL}/{settings.API_VERSION}/demix/{str(job_id)}"),
        HttpUrl(
            f"{settings.API_BASE_URL}/{settings.API_VERSION}/demix/{str(job_id)}/result"
        ),
        HttpUrl(
            f"{settings.API_BASE_URL}/{settings.API_VERSION}/demix/{str(job_id)}/cancel"
        ),
    )
