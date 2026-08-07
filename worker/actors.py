from uuid import UUID

import dramatiq

from worker.main import get_context


@dramatiq.actor
def process_demix(job_id: UUID):

    ctx = get_context()

    # todo: try except that manages job states and calls demix processor


@dramatiq.actor
def cleanup_expired_jobs(): ...
