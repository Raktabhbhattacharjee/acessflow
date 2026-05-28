from app.core.config import Settings
from app.dependencies import get_storage
from app.storage.local import LocalStorage
import pytest


def test_get_storage_returns_local_storage():
    config = Settings(storage_backend="local", storage_path="./test_uploads")
    storage = get_storage(config)
    assert isinstance(storage, LocalStorage)


def test_get_storage_accepts_uppercase_local():
    config = Settings(storage_backend="LOCAL", storage_path="./test_uploads")

    storage = get_storage(config)

    assert isinstance(storage, LocalStorage)


def test_get_storage_raises_error_for_invalid_backend():
    config = Settings(storage_backend="banana")

    with pytest.raises(ValueError) as error:
        get_storage(config)

    assert "Unsupported storage backend: banana" in str(error.value)



def test_get_storage_returns_s3_storage_without_real_aws(monkeypatch):
    class FakeS3Storage:
        def __init__(self, bucket_name, region_name):
            self.bucket_name = bucket_name
            self.region_name = region_name

    monkeypatch.setattr("app.dependencies.S3Storage", FakeS3Storage)

    config = Settings(
        storage_backend="s3",
        s3_bucket_name="fake-test-bucket",
        aws_region="ap-south-1",
    )

    storage = get_storage(config)

    assert isinstance(storage, FakeS3Storage)
    assert storage.bucket_name == "fake-test-bucket"
    assert storage.region_name == "ap-south-1"