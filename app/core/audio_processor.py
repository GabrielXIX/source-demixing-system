from dataclasses import dataclass
from pathlib import Path

from exceptions import InvalidAudioError, SDSException
from fastapi import UploadFile

from app.core.logger import logger

MAX_DURATION_SECONDS = 900  # 15 minutes
MIN_SAMPLE_RATE = 8000  # 8 kHz
MAX_SAMPLE_RATE = 192000  # 192 kHz
MAX_CHANNELS = 8
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


@dataclass
class ValidatedTrackMetadata:
    duration: int
    sample_rate: int
    num_channels: int


class AudioProcessor:
    def __init__(self):
        pass

    def validate_file(self, file: UploadFile):
        logger.debug("File validation started")

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

    def validate_track(self, file_path: Path):
        logger.debug("Track validation started")
        try:
            import torchaudio

            info = torchaudio.info(str(file_path))  # type: ignore
        except Exception as e:
            raise SDSException(
                f"Failed to read audio file metadata with torchaudio: {str(e)}"
            )

        duration = info.num_frames / info.sample_rate
        if duration <= 0 or duration > MAX_DURATION_SECONDS:
            raise InvalidAudioError(
                f"Audio duration: {duration} s, is out of the allowed range: > 0 - {MAX_DURATION_SECONDS} s"
            )

        sample_rate = info.sample_rate
        if sample_rate < MIN_SAMPLE_RATE or sample_rate > MAX_SAMPLE_RATE:
            raise InvalidAudioError(
                f"Sample rate: {sample_rate} Hz, is out of the allowed range: {MIN_SAMPLE_RATE} - {MAX_SAMPLE_RATE} Hz"
            )

        num_channels = info.num_channels
        if num_channels < 1 or num_channels > MAX_CHANNELS:
            raise InvalidAudioError(
                f"Number of channes: {num_channels}, is out of the allowed range: 1 - {MAX_CHANNELS}"
            )

        logger.debug("Track validation completed")
        return ValidatedTrackMetadata(
            duration=duration, sample_rate=sample_rate, num_channels=num_channels
        )
