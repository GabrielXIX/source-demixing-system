from dataclasses import dataclass

from exceptions import InvalidAudioError
from fastapi import UploadFile

from app.core.logger import logger

MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB
SUPPORTED_FILE_FORMATS = ["wav", "mp3"]
CONTENT_TYPE_MAP = {
    "audio/mpeg": ".mp3",
    "audio/mp3": ".mp3",
    "audio/wav": ".wav",
    "audio/wave": ".wav",
    "audio/x-wav": ".wav",
    "audio/flac": ".flac",
    "audio/aac": ".aac",
    "audio/ogg": ".ogg",
    "audio/m4a": ".m4a",
    "audio/opus": ".opus",
}


@dataclass
class ValidatedFileMetadata:
    content_type: str
    size: int
    filename: str
    extension: str


class AudioProcessor:
    def __init__(self):
        pass

    def validate_file(self, file: UploadFile):
        logger.debug("Starting file validation...")

        content_type = file.content_type
        if not content_type or content_type.startswith("audio/"):
            raise InvalidAudioError("Invalid content type")

        size = file.size
        if not size or size > MAX_FILE_SIZE or size == 0:
            raise InvalidAudioError("File size too large or 0")

        filename = file.filename
        if not filename:
            raise InvalidAudioError("No file name")

        extension = CONTENT_TYPE_MAP.get(content_type)
        if extension not in SUPPORTED_FILE_FORMATS:
            raise InvalidAudioError("Unsupported file extension")

        logger.debug("File validation completed")
        return ValidatedFileMetadata(
            content_type=content_type, size=size, filename=filename, extension=extension
        )

    def validate_track(self, file: UploadFile):
        # Validate duration

        # Validate sample rate

        # Validate channels

        pass
