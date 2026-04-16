from functools import lru_cache
from fastapi import Depends
from app.core.config import settings, Settings
from app.storage.base import StorageBackend
from app.storage.local import LocalStorage


@lru_cache
def get_settings() -> Settings:
    return settings


def get_storage(config: Settings = Depends(get_settings)) -> StorageBackend:
    return LocalStorage(config.storage_path)