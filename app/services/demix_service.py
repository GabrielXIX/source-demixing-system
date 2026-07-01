from fastapi import BackgroundTasks


class DemixService:
    """Orchestrates the demix process"""

    async def start_demix(self, data, background_tasks: BackgroundTasks):
        # 1. Save file to storage

        # 2. Validate file with audio processor

        # 3. Create job for state management

        # 4. Start background task (demucs engine, storage service, job manager)

        # 5. Return job id for added job
        pass
