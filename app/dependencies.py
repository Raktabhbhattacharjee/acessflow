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
    """
    Return the configured storage backend.

    Currently supported:
    - local: stores uploaded files on disk
    - s3: uploads files to Amazon S3

    Raises:
        ValueError: if an unsupported storage backend is configured.
    """
    if config.storage_backend == "local":
        return LocalStorage(config.storage_path)

    if config.storage_backend == "s3":
        return S3Storage(
            bucket_name=config.s3_bucket_name,
            region_name=config.aws_region,
        )

    raise ValueError(f"Unsupported storage backend: {config.storage_backend}")