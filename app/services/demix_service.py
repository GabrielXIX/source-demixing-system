from fastapi import BackgroundTasks


class DemixService:
    """Orchestrates the demix process"""

    async def start_demix(self, data, background_tasks: BackgroundTasks):
        try:
            # 1. Do basic file validation

            # 2. Create job

            # 3. Save file to storage
            # 3.1 Update job status

            # 4. Do deep file validation
            # 4.1 Update job status
            # 4.2 Delete file if deep validation fails

            # 5. Save metadata
            # 5.1 Update job status

            # 6. Start background task (demucs engine, storage service, job manager)
            # 6.1 Update job status

            # 5. Return job id for added job
            pass
        except Exception as e:
            # re raise to router
            pass
