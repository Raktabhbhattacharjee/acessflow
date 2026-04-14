from abc import ABC, abstractmethod
from fastapi import UploadFile

class StorageBackend(ABC):
    @abstractmethod
    async def save(self, file_bytes: bytes, filename: str) -> str: ...