import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.dependencies import get_storage


class FakeStorage:
    """
    Fake storage used only for tests.

    It behaves like a real storage backend because it has an async save()
    method, but it does not write to local disk or S3.

    The save_called flag lets the test prove whether storage.save()
    was touched or not.
    """

    def __init__(self):
        self.save_called = False
        self.saved_filename = None
        self.saved_bytes = None

    async def save(self, file_bytes, filename):
        """
        Fake version of storage.save().

        If this method runs, it means the upload route reached the storage step.
        """
        self.save_called = True
        self.saved_filename = filename
        self.saved_bytes = file_bytes
        return f"fake/{filename}"


@pytest.fixture
def fake_storage():
    storage = FakeStorage()

    app.dependency_overrides[get_storage] = lambda: storage

    yield storage

    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


def test_invalid_upload(client, fake_storage):
    response = client.post(
        "/upload/",
        files={
            "file": (
                "virus.exe",
                b"fake file content",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert fake_storage.save_called is False


def test_empty_upload(client, fake_storage):
    response = client.post(
        "/upload/",
        files={
            "file": (
                "empty.txt",
                b"",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert fake_storage.save_called is False


def test_valid_upload(client, fake_storage):
    response = client.post(
        "/upload/",
        files={
            "file": (
                "notes.txt",
                b"hello accessflow",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200
    assert fake_storage.save_called is True
    assert fake_storage.saved_filename == "notes.txt"
    assert fake_storage.saved_bytes == b"hello accessflow"

    data = response.json()

    assert data["status"] == "success"
    assert data["error"] is None
    assert data["data"]["filename"] == "notes.txt"
    assert data["data"]["content_type"] == "text/plain"
    assert data["data"]["size_bytes"] == len(b"hello accessflow")
    assert data["data"]["storage_reference"] == "fake/notes.txt"


def test_large_upload(client, fake_storage):
    response = client.post(
        "/upload/",
        files={
            "file": (
                "big.txt",
                b"x" * (6 * 1024 * 1024),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert fake_storage.save_called is False


class BrokenStorage:
    async def save(self, file_bytes, filename):
        raise RuntimeError("storage is down")


def test_storage_failure(client):
    broken_storage = BrokenStorage()

    app.dependency_overrides[get_storage] = lambda: broken_storage

    response = client.post(
        "/upload/",
        files={
            "file": (
                "notes.txt",
                b"hello accessflow",
                "text/plain",
            )
        },
    )

    app.dependency_overrides.clear()

    assert response.status_code == 500

    data = response.json()

    assert data["status"] == "error"
    assert data["data"] is None
    assert data["error"] == "Internal server error"


def test_invalid_upload(client, fake_storage):
    response = client.post(
        "/upload/",
        files={
            "file": (
                "virus.exe",
                b"fake file content",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert fake_storage.save_called is False

    data = response.json()

    assert data["status"] == "error"
    assert data["data"] is None
    assert data["error"] is not None
