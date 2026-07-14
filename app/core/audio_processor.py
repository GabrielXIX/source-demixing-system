from pathlib import Path

from exceptions import InvalidAudioError
from fastapi import UploadFile

from app.core.logger import logger

MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB
SUPPORTED_FILE_FORMATS = ["wav", "mp3"]


class AudioProcessor:
    def __init__(self):
        pass

    def validate_file(self, file: UploadFile):
        logger.debug("Starting file validation...")

        if not file.content_type or file.content_type.startswith("audio/"):
            raise InvalidAudioError("Invalid file type")

        if not file.size or file.size > MAX_FILE_SIZE:
            raise InvalidAudioError("File size too large")

        if not file.filename:
            raise InvalidAudioError("No file name")

        extension = Path(file.filename).suffix.lower()
        if extension not in SUPPORTED_FILE_FORMATS:
            raise InvalidAudioError("Unsupported file extension")

        logger.debug("File validation completed")

    def validate_track(self, file: UploadFile):
        # Validate duration

        # Validate sample rate

        # Validate channels

        pass
