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

    async def save(self, file_bytes, filename):
        """
        Fake version of storage.save().

        If this method runs, it means the upload route reached the storage step.
        For invalid files, this should NOT happen.
        """
        self.save_called = True
        return f"fake/{filename}"


def test_invalid_upload():
    """
    Invalid uploads should be rejected before storage is touched.

    This test replaces the real storage dependency with FakeStorage,
    uploads a dangerous .exe file, and checks two things:

    1. The API returns 400 Bad Request.
    2. FakeStorage.save() was never called.
    """
    fake_storage = FakeStorage()

    # Replace real get_storage() with a test version that returns FakeStorage.
    app.dependency_overrides[get_storage] = lambda: fake_storage

    client = TestClient(app)

    response = client.post(
        "/upload/",
        files={
            "file": (
                "virus.exe",
                "fake file content",
                "text/plain",
            )
        },
    )

    # Clean up dependency override so it does not affect other tests.
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
