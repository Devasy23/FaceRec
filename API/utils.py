from __future__ import annotations

import logging


def init_logging_config():
    """
    Initializes the logging configuration. This function sets up a custom formatter
    for logging which prints colored logs. The logs are written to both the console
    and a file.

    The custom formatter prints logs in the following format:

        %(asctime)s (%(filename)s:%(lineno)d) - %(levelname)s: %(message)s

    The colors used for the log levels are as follows:

        DEBUG: blue
        INFO: green
        WARNING: yellow
        ERROR: red
        CRITICAL: bold red

    The logs are written to both the console and a file. The file is named 'app.log'
    and is written in the same directory as the script. The file is overwritten each
    time the script is run. The logs are written in the same format as the console
    logs, but without colors.
    """

    # This class defines a custom logging formatter in Python.
    class CustomFormatter(logging.Formatter):
        def __init__(self, file=False):
            """
            Custom log formatter that prints colored logs.

            Args:
                file (bool, optional): If true, the log format will not include colors. Defaults to False.
            """
            super().__init__()
            yellow = "\x1b[36;10m" if not file else ""
            blue = "\x1b[35;10m" if not file else ""
            green = "\x1b[32;10m" if not file else ""
            red = "\x1b[31;10m" if not file else ""
            bold_red = "\x1b[31;1m" if not file else ""
            reset = "\x1b[0m" if not file else ""
            log = "%(asctime)s (%(filename)s:%(lineno)d) - %(levelname)s: "
            msg = reset + "%(message)s"

            self.FORMATS = {
                logging.DEBUG: blue + log + msg,
                logging.INFO: green + log + msg,
                logging.WARNING: yellow + log + msg,
                logging.ERROR: red + log + msg,
                logging.CRITICAL: bold_red + log + msg,
            }

        def format(self, record):
            """
            Format a record with the corresponding color.

            Args:
                record (logging.LogRecord): The log record to format.

            Returns:
                str: The formatted log record.
            """
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.DEBUG)
    stderr_handler.setFormatter(CustomFormatter())
    logger.addHandler(stderr_handler)

    file_handler = logging.FileHandler("app.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(CustomFormatter(True))
    logger.addHandler(file_handler)
