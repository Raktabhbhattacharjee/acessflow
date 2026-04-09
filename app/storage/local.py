import os

UPLOAD_DIR = "uploads"


class LocalStorage:
    def save(self, file_bytes, filename):
        print(f"💾 Storage: saving {filename}")

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        print(f"📦 Storage: saved at {file_path}")

        return file_path