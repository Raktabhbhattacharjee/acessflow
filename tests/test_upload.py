import tempfile
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_storage
from app.storage.local import LocalStorage

def get_test_storage():
    return LocalStorage(tempfile.mkdtemp())

app.dependency_overrides[get_storage] = get_test_storage

client = TestClient(app)

def test_upload_valid_file():
    response = client.post(
        "/upload/",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["filename"] == "test.txt"

def test_upload_invalid_file_type():
    response = client.post(
        "/upload/",
        files={"file": ("test.pdf", b"some content", "application/pdf")}
    )
    assert response.status_code == 400
    assert response.json()["status"] == "error"