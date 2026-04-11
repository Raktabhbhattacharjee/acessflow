from app.core.exceptions import AppException


def validate_file(file):

    if not file.filename or file.filename.strip() == "":
        raise AppException("Invalid file: no filename")

    if file.content_type not in ["text/plain", "image/jpeg", "image/png"]:
        raise AppException("Invalid file type")

    return True
