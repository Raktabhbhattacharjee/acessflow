import pytest
from app.validators.file_validator import validate_file
from app.core.exceptions import AppException


class FakeUploadFile:
    def __init__(self, filename, content_type):
        self.filename = filename
        self.content_type = content_type


def test_empty_filename():
    file = FakeUploadFile(filename="", content_type="text/plain")

    with pytest.raises(AppException):
        validate_file(file)


def test_blank_filename():
    file = FakeUploadFile(filename="   ", content_type="text/plain")

    with pytest.raises(AppException):
        validate_file(file)


def test_invalid_file_type():
    file = FakeUploadFile(filename="script.js", content_type="application/javascript")

    with pytest.raises(AppException):
        validate_file(file)


def test_dangerous_extension():
    file = FakeUploadFile(filename="virus.exe", content_type="text/plain")

    with pytest.raises(AppException):
        validate_file(file)


def test_zero_byte_file():
    file=FakeUploadFile(filename="empty.txt",content_type="text/plain")
    with pytest.raises(AppException):
        validate_file(file,size_bytes=0)

def test_oversized_file():
    file = FakeUploadFile(filename="big.txt", content_type="text/plain")

    with pytest.raises(AppException):
        validate_file(file, size_bytes=6 * 1024 * 1024)