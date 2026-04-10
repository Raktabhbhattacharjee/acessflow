from app.storage.local import LocalStorage
from app.core.logger import get_logger

storage = LocalStorage()
logger = get_logger("file_service")


def handle_upload(file_bytes, filename):
    logger.info(f"Handling file: {filename}")

    try:
        path = storage.save(file_bytes, filename)

        logger.info(f"File saved successfully: {path}")
        return path

    except Exception as e:
        logger.error(
            f"Service error while handling {filename}: {str(e)}",
            exc_info=True
        )
        raise