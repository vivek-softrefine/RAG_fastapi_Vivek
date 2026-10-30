import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LogUtils:
    """Configure and manage application logging."""

    @staticmethod
    def configure_logging() -> None:
        """Configure logging based on environment variables."""

        log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_name, None)

        if not isinstance(log_level, int):
            raise ValueError(f"Invalid logging level: {log_level_name}")

        # File logging is optional; enable with LOG_TO_FILE=true.
        log_to_file = os.getenv("LOG_TO_FILE", "false").lower() == "true"

        log_format = (
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        )

        formatter = logging.Formatter(log_format)

        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        if getattr(root_logger, "_app_configured", False):
            return

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        if log_to_file:
            log_directory = Path("logs")
            log_directory.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_directory / "app.log",
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)

        root_logger._app_configured = True

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Return a logger for the requested module."""

        return logging.getLogger(name)