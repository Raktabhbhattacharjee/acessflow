import os
from app.core.logger import get_logger

UPLOAD_DIR = "uploads"
logger = get_logger("local_storage")


class LocalStorage:
    def save(self, file_bytes, filename):
        logger.info(f"Saving file: {filename}")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        logger.info(f"File stored at: {file_path}")

        return file_path