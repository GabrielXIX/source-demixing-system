from fastapi import Request

from app.services.demix_service import DemixService


def get_demix_service(request: Request) -> DemixService:
    return request.app.state.demix_service
