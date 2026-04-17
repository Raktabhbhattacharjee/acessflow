import logging
import sys
import os
import json
from app.core.context import request_id_context


class JsonFormatter(logging.Formatter):
    def format(self, record):
        message = record.msg

        # Get request_id from context if available
        request_id = request_id_context.get()

        log_record = {
            "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": message if isinstance(message, dict) else record.getMessage(),
        }

        # Add request_id if it exists and is not already in the message
        if request_id:
            log_record["request_id"] = request_id

        return json.dumps(log_record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    logger.propagate = False

    return logger
