import os
from app.core.logger import get_logger
from app.storage.base import StorageBackend

logger = get_logger("local_storage")


class LocalStorage(StorageBackend):
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    async def save(self, file_bytes: bytes, filename: str) -> str:
        logger.info(f"Saving file: {filename}")
        os.makedirs(self.storage_path, exist_ok=True)
        file_path = os.path.join(self.storage_path, filename)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        logger.info(f"File stored at: {file_path}")
        return file_path

    def ensure_directory(self) -> None:
        os.makedirs(self.storage_path, exist_ok=True)
        logger.info("storage.local.directory_ready", extra={"path": self.storage_path})