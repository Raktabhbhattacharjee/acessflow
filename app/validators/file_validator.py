from app.core.exceptions import AppException

DANGEROUS_EXTENSIONS = [".exe", ".js", ".bat", ".cmd", ".sh"]
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

def validate_file(file, size_bytes=None):

    if not file.filename or file.filename.strip() == "":
        raise AppException("Invalid file: no filename")

    filename = file.filename.lower()

    for extension in DANGEROUS_EXTENSIONS:
        if filename.endswith(extension):
            raise AppException("Invalid file: dangerous extension")

    if file.content_type not in ["text/plain", "image/jpeg", "image/png"]:
        raise AppException("Invalid file type")

    if size_bytes == 0:
        raise AppException("Invalid file: empty file")

    if size_bytes is not None and size_bytes > MAX_FILE_SIZE_BYTES:
        raise AppException('Invalid file: file too large')
    return True
