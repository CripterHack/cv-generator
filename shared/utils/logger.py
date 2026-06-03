import logging
import sys
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
from datetime import datetime
import json
from typing import Dict, Any
import traceback


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after gathering all the log record args
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the record as JSON
        """
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }

        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id

        if record.exc_info:
            log_obj["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info),
            }

        if hasattr(record, "duration"):
            log_obj["duration_ms"] = record.duration

        return json.dumps(log_obj)


class Logger:
    """
    Enhanced logger with additional features and better formatting
    """

    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        log_level: str = "INFO",
        json_output: bool = True,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)

        # File handler with size-based rotation
        size_handler = RotatingFileHandler(
            os.path.join(log_dir, f"{name}.log"),
            maxBytes=max_bytes,
            backupCount=backup_count,
        )

        # File handler with time-based rotation (daily)
        time_handler = TimedRotatingFileHandler(
            os.path.join(log_dir, f"{name}_daily.log"),
            when="midnight",
            interval=1,
            backupCount=30,
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)

        # Set formatter based on json_output flag
        if json_output:
            formatter = JsonFormatter()
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s - (%(filename)s:%(lineno)d)"
            )

        # Set formatters
        size_handler.setFormatter(formatter)
        time_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(size_handler)
        self.logger.addHandler(time_handler)
        self.logger.addHandler(console_handler)

    def _log_with_context(
        self, level: int, message: str, extra: Dict[str, Any] = None
    ) -> None:
        """
        Log with additional context
        """
        if extra is None:
            extra = {}
        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, **kwargs: Any) -> None:
        self._log_with_context(logging.DEBUG, message, kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self._log_with_context(logging.INFO, message, kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self._log_with_context(logging.WARNING, message, kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self._log_with_context(logging.ERROR, message, kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self._log_with_context(logging.CRITICAL, message, kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        if "exc_info" not in kwargs:
            kwargs["exc_info"] = True
        self._log_with_context(logging.ERROR, message, kwargs)


# Create application loggers with enhanced features
cv_logger = Logger(
    "cv_generator", log_level=os.getenv("LOG_LEVEL", "INFO"), json_output=True
)

api_logger = Logger("api", log_level=os.getenv("LOG_LEVEL", "INFO"), json_output=True)

frontend_logger = Logger(
    "frontend", log_level=os.getenv("LOG_LEVEL", "INFO"), json_output=True
)
