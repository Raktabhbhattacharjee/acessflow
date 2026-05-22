# AccessFlow

A backend architecture project for file ingestion with pluggable storage backends (local or AWS S3).

**Focus:** Clean separation of responsibilities, configuration-driven backends, and testable design.

## Architecture Overview

```mermaid
flowchart TD
    A[User uploads file] --> B[FastAPI /upload/ route]
    B --> C[FileValidator]
    C --> D[get_storage]
    D --> E{STORAGE_BACKEND<br/>config}
    E -->|local| F[LocalStorage]
    E -->|s3| G[S3Storage]
    F --> H[Save to ./uploads]
    G --> I[Upload to S3 bucket]
    H --> J[Return storage_reference]
    I --> J
    J --> K[API success response]
```

**Design principle:** The upload route depends on the abstract `StorageBackend` interface, not concrete implementations. Storage choice is configuration-driven and decoupled from business logic.

## Components

| Component                  | Responsibility                                  |
| -------------------------- | ----------------------------------------------- |
| `POST /upload/`            | Coordinate upload flow (validation + storage)   |
| `GET /health`              | Health check for load balancers                 |
| `FileValidator`            | Validate file extension, name, and size         |
| `StorageBackend`           | Abstract interface for storage implementations  |
| `LocalStorage`             | **Local backend:** Save files to `./uploads`    |
| `S3Storage`                | **S3 backend:** Upload files to AWS S3          |
| `RequestLoggingMiddleware` | Log all requests with request_id and latency_ms |

**Key:** S3-specific logic stays in `S3Storage`, local file logic stays in `LocalStorage`. The upload route never knows which backend is active—it just calls `storage.save()`. Selection happens in `get_storage()`.

## Project Structure

```
app/
├── main.py                 # FastAPI app initialization
├── dependencies.py         # Dependency injection (get_settings, get_storage)
├── core/
│   ├── config.py           # Pydantic Settings (env vars)
│   ├── exceptions.py       # Error handlers
│   ├── logger.py           # JSON logging
│   ├── middleware.py       # Request logging middleware
│   └── responses.py        # Standard response models
├── routes/
│   ├── health.py           # GET /health
│   └── upload.py           # POST /upload/
├── validators/
│   └── file_validator.py   # File validation
└── storage/
    ├── base.py             # StorageBackend abstract class
    ├── local.py            # LocalStorage implementation
    └── s3.py               # S3Storage implementation

tests/
├── conftest.py             # Pytest fixtures and dependency overrides
├── test_health.py
└── test_upload.py

scripts/
├── create_s3_bucket.ps1    # Create S3 bucket for testing
└── delete_s3_bucket.ps1    # Delete S3 bucket and all objects
```

## Environment Variables

```env
# App
APP_NAME=AccessFlow
APP_VERSION=1.0.0
DEBUG=false

# Storage
STORAGE_BACKEND=local
STORAGE_PATH=./uploads

# AWS (required for STORAGE_BACKEND=s3)
AWS_REGION=ap-south-1
S3_BUCKET_NAME=accessflow-uploads-raktabh-2026

# Logging
LOG_LEVEL=INFO

# Upload limits
MAX_UPLOAD_SIZE_MB=100
```

**Important:** Do not commit `.env` to version control.

## Running the App

### Setup

```bash
cd acessflow
uv venv
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate   # macOS/Linux
uv sync
cp .env.example .env
```

### Start Development Server

```bash
uv run python -m uvicorn app.main:app --reload
```

Server runs at `http://127.0.0.1:8000`

### Docker

```bash
docker build -t accessflow:latest .
docker run -p 8000:8000 -e STORAGE_BACKEND=local accessflow:latest
```

## Testing

### Local Storage Upload

1. Ensure `STORAGE_BACKEND=local` in `.env`
2. Upload a file:

```bash
curl.exe -X POST "http://127.0.0.1:8000/upload/" -F "file=@test.txt"
```

3. Expected response:

```json
{
  "status": "success",
  "data": {
    "filename": "test.txt",
    "storage_backend": "local",
    "storage_reference": "uploads/test.txt",
    "size_bytes": 38,
    "content_type": "text/plain"
  },
  "error": null
}
```

4. Verify file in `./uploads` directory

### S3 Storage Upload

**Prerequisites:**

- AWS CLI configured with credentials
- S3 bucket created

1. Set `STORAGE_BACKEND=s3` in `.env`
2. Upload a file:

```bash
curl.exe -X POST "http://127.0.0.1:8000/upload/" -F "file=@test.txt"
```

3. Expected response:

```json
{
  "status": "success",
  "data": {
    "filename": "test.txt",
    "storage_backend": "s3",
    "storage_reference": "uploads/550e8400-e29b-41d4-a716-446655440000.txt",
    "size_bytes": 38,
    "content_type": "text/plain"
  },
  "error": null
}
```

4. Verify file in S3:

```bash
aws s3 ls s3://accessflow-uploads-raktabh-2026/uploads/
```

### Important: Trailing Slash

The upload endpoint **requires** a trailing slash: `/upload/`

Correct: `http://127.0.0.1:8000/upload/`
Incorrect: `http://127.0.0.1:8000/upload` (causes 307 redirect)

## Response Format

All responses follow this envelope:

```json
{
  "status": "success",
  "data": {
    "filename": "test.txt",
    "storage_backend": "local",
    "storage_reference": "uploads/test.txt",
    "size_bytes": 1024,
    "content_type": "text/plain"
  },
  "error": null
}
```

On error:

```json
{
  "status": "error",
  "data": null,
  "error": "File size exceeds maximum of 100 MB"
}
```

## S3 Bucket Scripts

### Create Bucket

```powershell
.\scripts\create_s3_bucket.ps1
```

Creates a private S3 bucket with "Block Public Access" enabled using values from `.env`:

- `S3_BUCKET_NAME` — bucket name
- `AWS_REGION` — bucket region

### Delete Bucket

```powershell
.\scripts\delete_s3_bucket.ps1
```

Deletes all objects in the bucket, then deletes the empty bucket. Enables repeatable S3 testing.

**Workflow:**

```
1. Create bucket: .\scripts\create_s3_bucket.ps1
2. Upload files and test
3. Clean up: .\scripts\delete_s3_bucket.ps1
4. Repeat from step 1
```

## Running Tests

Run all tests:

```bash
uv run pytest tests/ -v
```

Run specific test file:

```bash
uv run pytest tests/test_upload.py -v
```

Run with coverage:

```bash
uv run pytest tests/ --cov=app --cov-report=term-missing
```

Tests use dependency injection to inject mock storage, preventing file I/O and S3 calls during testing.

## Storage Backend Design

### How It Works

**Dependency Injection:** `get_storage()` returns the active `StorageBackend` based on `STORAGE_BACKEND` env var.

```python
# upload.py never knows which backend is active
storage = get_storage()  # Returns LocalStorage or S3Storage
reference = storage.save(file_bytes, filename)
```

### Local vs S3 Mode

| Aspect                | Local                               | S3                                                   |
| --------------------- | ----------------------------------- | ---------------------------------------------------- |
| **Backend selection** | `STORAGE_BACKEND=local`             | `STORAGE_BACKEND=s3`                                 |
| **File saved to**     | `./uploads/` directory              | AWS S3 bucket                                        |
| **Storage reference** | `uploads/filename.txt`              | `uploads/uuid-filename.txt` (renamed for uniqueness) |
| **Use case**          | Development, testing, single-server | Production, multi-region, shared infrastructure      |
| **Logic location**    | `app/storage/local.py`              | `app/storage/s3.py`                                  |

### Separation of Concerns

- **`upload.py`** — Orchestrates the upload flow. Calls `validate_file()`, `get_storage()`, and `storage.save()`. Never has S3-specific logic.
- **`local.py`** — All local file handling: opening directories, writing files, generating references.
- **`s3.py`** — All S3-specific logic: bucket operations, client configuration, UUID generation, S3 API calls.
- **`get_storage()`** — The only place that decides which backend to use. Changes to this function are the only reason to edit `dependencies.py`.

This design makes it easy to:

- Add a new backend (e.g., Azure Blob) without touching `upload.py`
- Test the upload route with mock storage
- Swap backends by changing one environment variable

## Security Notes

- Do not commit `.env` (contains secrets)
- On AWS, use IAM roles instead of hardcoded credentials
- Keep S3 buckets private with "Block Public Access" enabled
- Use least-privilege IAM policies for S3 access
