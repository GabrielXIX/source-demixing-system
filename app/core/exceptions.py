class SDSException(Exception):
    pass


class InvalidAudioError(SDSException):
    pass


class JobNotFoundError(SDSException):
    pass


# Python built in errors used in the project:
# KeyError, TypeError
