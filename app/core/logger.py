import logging
import sys
import os


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Always set level — must be outside handler guard
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Stop logs bubbling to root logger (prevents duplicate output)
    logger.propagate = False

    return logger