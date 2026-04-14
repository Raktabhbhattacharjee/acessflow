import os
from app.core.config import settings
from app.core.logger import get_logger
from app.storage.base import StorageBackend

logger = get_logger("local_storage")

class LocalStorage(StorageBackend):
    async def save(self, file_bytes: bytes, filename: str) -> str:
        logger.info(f"Saving file: {filename}")
        os.makedirs(settings.storage_path, exist_ok=True)
        file_path = os.path.join(settings.storage_path, filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"File stored at: {file_path}")
        return file_path