import logging


class Logger:
    def __init__(self):
        # Set logger variables, format, file context
        self.logger = logging.getLogger()

    def log_info(self, message: str):
        self.logger.info(message)
