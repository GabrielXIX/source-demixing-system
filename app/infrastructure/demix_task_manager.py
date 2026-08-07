from uuid import UUID

from worker.actors import (
    cleanup_expired_jobs,
    process_demix,
)


class DemixTaskManager:
    def enqueue_demix(self, job_id: UUID) -> None:
        process_demix.send(job_id)

    def enqueue_cleanup(self) -> None:
        cleanup_expired_jobs.send()
