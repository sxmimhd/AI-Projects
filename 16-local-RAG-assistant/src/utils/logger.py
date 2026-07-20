import logging
from pathlib import Path

from config import settings


class Logger:
    _logger = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is not None:
            return cls._logger

        Path(settings.LOGS_DIR).mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(settings.PROJECT_NAME)
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
        logger.propagate = False

        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            settings.LOG_FILE,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        cls._logger = logger

        return logger