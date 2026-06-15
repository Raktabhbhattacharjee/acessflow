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
        For invalid files, this should NOT happen.
        """
        self.save_called = True
        self.saved_filename = filename
        self.saved_bytes = file_bytes
        return f"fake/{filename}"


def test_invalid_upload():
    """
    Invalid uploads should be rejected before storage is touched.
    """
    fake_storage = FakeStorage()

    app.dependency_overrides[get_storage] = lambda: fake_storage

    client = TestClient(app)

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

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert fake_storage.save_called is False


def test_empty_upload():
    fake_storage = FakeStorage()

    app.dependency_overrides[get_storage] = lambda: fake_storage

    client = TestClient(app)

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

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert fake_storage.save_called is False


def test_valid_upload():
    fake_storage = FakeStorage()

    app.dependency_overrides[get_storage] = lambda: fake_storage

    client = TestClient(app)

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

    assert response.status_code == 200
    assert fake_storage.save_called is True
    assert fake_storage.saved_filename == "notes.txt"
    assert fake_storage.saved_bytes == b"hello accessflow"
