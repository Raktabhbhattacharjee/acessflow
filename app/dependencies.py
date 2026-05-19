from functools import lru_cache
from fastapi import Depends
from app.core.config import settings, Settings
from app.storage.base import StorageBackend
from app.storage.local import LocalStorage
from app.storage.s3 import S3Storage


@lru_cache
def get_settings() -> Settings:
    return settings


def get_storage(config: Settings = Depends(get_settings)) -> StorageBackend:
    storage_backend = config.storage_backend.lower()

    if storage_backend == "local":
        return LocalStorage(config.storage_path)

    if storage_backend == "s3":
        return S3Storage(
            bucket_name=config.s3_bucket_name,
            region_name=config.aws_region,
        )

    raise ValueError(f"Unsupported storage backend: {config.storage_backend}")