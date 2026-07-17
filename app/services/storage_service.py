from pathlib import Path
from uuid import UUID

from fastapi import UploadFile

from app.core.config import settings
from app.core.logger import logger


class StorageService:
    def __init__(self):
        self.base_path = Path(settings.STORAGE_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_input(self, job_id: UUID, file: UploadFile, extension: str) -> Path:
        logger.debug("Saving input to disk started")
        track_dir = self.base_path / str(job_id)
        file_path = track_dir / f"input{extension}"

        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # 1MB chunks
                f.write(chunk)

        logger.debug("Saving input to disk completed")
        return track_dir

    def save_track_metadata(self, job_id, metadata):
        pass
