from fastapi import Request

from app.services.demix_orchestrator import DemixOrchestrator


def get_demix_orchestrator(request: Request) -> DemixOrchestrator:
    return request.app.state.demix_orchestrator
