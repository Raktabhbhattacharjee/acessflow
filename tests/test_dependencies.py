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
