from fastapi import UploadFile


class AudioProcessor:
    def __init__(self):
        pass

    def validate_track_basic(self, file: UploadFile):
        # Validate file type

        # Validate file size

        # Validate file extension

        pass

    def validate_track_deep(self, file: UploadFile):
        # Validate duration

        # Validate sample rate

        # Validate channels

        pass
