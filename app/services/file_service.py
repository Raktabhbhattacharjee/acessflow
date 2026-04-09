from app.storage.local import LocalStorage

storage = LocalStorage()


def handle_upload(file_bytes, filename):
    print(f"⚙️ Service: handling file -> {filename}")

    try:
        path = storage.save(file_bytes, filename)

        print(f"✅ Service: file saved at {path}")

        return path

    except Exception as e:
        print(f"❌ Service error: {str(e)}")
        raise e