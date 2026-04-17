# AccessFlow

[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.135+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)

A production-ready backend learning project demonstrating clean FastAPI architecture, structured observability, and cloud readiness. Built to master real-world patterns: middleware, dependency injection, abstract storage backends, and containerization.

## Overview

AccessFlow is **not a feature-heavy application**—it's a deliberate study in architecture. The goal is to build a single, well-architected file upload service that showcases:

- ✅ **Clean request flow** with request IDs and latency tracking
- ✅ **Structured JSON logging** (CloudWatch-ready)
- ✅ **Dependency injection** for testability and flexibility
- ✅ **Pluggable storage backends** (LocalStorage → S3 swap by adding one class)
- ✅ **AWS-ready patterns** (ALB health checks, CloudWatch integration)
- ✅ **Production Docker** (multi-stage builds, non-root user)
- ✅ **Integration testing** with DI overrides
- ✅ **Standardized responses** across all endpoints

## Stack

| Component           | Choice                  | Why                                          |
| ------------------- | ----------------------- | -------------------------------------------- |
| **Language**        | Python 3.13+            | Modern, clear, fast enough                   |
| **Framework**       | FastAPI                 | Async, Pydantic validation, auto docs        |
| **Config**          | pydantic-settings       | Type-safe env vars, .env support             |
| **Package Manager** | uv                      | Fast, deterministic, Python 3.13 native      |
| **Container**       | Docker (multi-stage)    | Lightweight, non-root user, production-grade |
| **Storage**         | Local (pluggable to S3) | No vendor lock-in, easy to extend            |

## Architecture

```
Request IN (with User-Agent, Content-Type, etc.)
    ↓
RequestLoggingMiddleware
    ├── Generate request_id (UUID)
    ├── Record start_time
    └── Attach to request state
    ↓
Route Handler (FastAPI)
    ├── Depends(get_storage) → StorageBackend ABC
    ├── Depends(get_settings) → Settings (from .env)
    └── Route logic
    ↓
Validator (FileValidator)
    ├── Check file extension (whitelist)
    ├── Check filename (no traversal)
    └── Check file size (if configured)
    ↓
StorageBackend.save()
    ├── LocalStorage (writes to ./uploads)
    └── S3Storage (future implementation)
    ↓
Response OUT (standardized format)
    {
      "status": "success|error",
      "data": {...},
      "error": null|{message, code}
    }
    ↓
ResponseLoggingMiddleware
    ├── Calculate latency_ms
    ├── Log as structured JSON
    └── Emit to stdout (piped to CloudWatch)
```

## What's Built ✨

### Core Infrastructure

- **Structured JSON Logging** — Every event logged with request_id, latency_ms, level, message
- **Pydantic Settings** — Type-safe configuration, reads .env, environment variables
- **Custom AppException** — Centralized error handler, converts to standardized response
- **RequestLoggingMiddleware** — Injects request_id, captures latency, logs structured format

### Routes

- **POST /upload** — File upload with validation, returns file metadata
- **GET /health** — AWS ALB-compatible health check

### Storage Layer

- **StorageBackend** (ABC) — Abstract base class for pluggable storage
- **LocalStorage** — Default implementation, writes to ./uploads (easily swappable to S3)

### Application Lifecycle

- **Lifespan Handler** — Startup: create upload directory, Shutdown: cleanup
- **Dependency Injection** — get_settings(), get_storage() as request-scoped dependencies

### Validation

- **FileValidator** — Extension whitelist, filename validation (no path traversal), size checks

### Testing

- **Integration Tests** — Tests for /health and /upload with DI overrides
- **Test Fixtures** — DI-aware test setup using conftest.py

### DevOps

- **Multi-Stage Docker** — Builder stage (compile/install), runtime stage (slim, non-root user)
- **Non-Root User** — Runs as appuser, not root (security best practice)

## What's Intentionally NOT Here 🚫

- ❌ **No Database** — This is file storage focused, not data warehousing
- ❌ **No SQLAlchemy** — No ORM overhead; file metadata only in memory/response
- ❌ **No Authentication** — Focus on architecture, not security theater
- ❌ **No Rate Limiting** — That's an ALB job, not an app concern
- ❌ **No GraphQL** — REST is simpler for file uploads

## Project Structure

```
.
├── app/
│   ├── main.py                    # FastAPI app initialization, routes registration
│   ├── dependencies.py            # get_settings(), get_storage() injection
│   ├── core/
│   │   ├── config.py              # Pydantic Settings model
│   │   ├── exceptions.py          # AppException, error handler
│   │   ├── lifespan.py            # @asynccontextmanager for startup/shutdown
│   │   ├── logger.py              # Structured logging configuration
│   │   ├── middleware.py          # RequestLoggingMiddleware
│   │   └── responses.py           # StandardResponse base model
│   ├── routes/
│   │   ├── health.py              # GET /health endpoint
│   │   └── upload.py              # POST /upload endpoint
│   ├── validators/
│   │   └── file_validator.py      # FileValidator for extension, name, size
│   └── storage/
│       ├── base.py                # StorageBackend abstract base class
│       └── local.py               # LocalStorage implementation
├── tests/
│   ├── conftest.py                # Pytest fixtures, DI overrides
│   ├── test_health.py             # Tests for /health endpoint
│   └── test_upload.py             # Tests for /upload endpoint
├── Dockerfile                     # Multi-stage, production-grade
├── pyproject.toml                 # Project metadata, dependencies, scripts
├── .env.example                   # Environment variable template
└── README.md                       # This file
```

## Quick Start

### Prerequisites

- Python 3.13+
- Docker (optional, for containerized setup)

### Local Setup with uv

1. **Clone and navigate to project:**

   ```bash
   cd accessflow
   ```

2. **Create virtual environment (uv handles this):**

   ```bash
   uv venv
   source .venv/bin/activate    # On macOS/Linux
   # or
   .venv\Scripts\Activate.ps1   # On Windows PowerShell
   ```

3. **Install dependencies:**

   ```bash
   uv sync
   ```

4. **Configure environment:**

   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults work locally)
   ```

5. **Run development server:**

   ```bash
   uv run fastapi dev app/main.py
   ```

   Server runs at `http://localhost:8000`

6. **Test the endpoints:**

   ```bash
   # Health check
   curl http://localhost:8000/health

   # File upload
   curl -X POST -F "file=@path/to/file.txt" \
     http://localhost:8000/upload
   ```

7. **Run integration tests:**
   ```bash
   uv run pytest tests/ -v
   ```

### Docker Setup

1. **Build image:**

   ```bash
   docker build -t accessflow:latest .
   ```

2. **Run container:**

   ```bash
   docker run -p 8000:8000 \
     -v $(pwd)/uploads:/app/uploads \
     accessflow:latest
   ```

3. **Test from host:**
   ```bash
   curl http://localhost:8000/health
   ```

### Project Commands

```bash
# Run dev server with auto-reload
uv run fastapi dev app/main.py

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app tests/

# Format code (if configured)
uv run black app/ tests/

# Lint
uv run ruff check app/ tests/
```

## Environment Variables

Create a `.env` file (or `.env.example` as template):

```env
# Application
APP_NAME=AccessFlow
APP_VERSION=1.0.0
DEBUG=false

# Storage
STORAGE_PATH=./uploads
MAX_UPLOAD_SIZE_MB=100

# Logging
LOG_LEVEL=INFO
```

All variables are validated by Pydantic Settings on startup.

## Integration Testing

Tests use FastAPI's `TestClient` with dependency overrides for full control:

```bash
uv run pytest tests/ -v
```

Tests demonstrate:

- ✅ Health check endpoint
- ✅ File upload with validation
- ✅ Error handling (invalid files)
- ✅ Dependency injection in tests

## Next Steps 🚀

### Short Term

- [ ] **S3 Storage Swap** — Implement `S3Storage(StorageBackend)` and swap in prod
- [ ] **Configuration as Code** — Read config from environment on startup
- [ ] **More Validators** — Add virus scanning, image metadata extraction

### Medium Term

- [ ] **AWS ECS Fargate** — Container orchestration, CloudWatch integration
- [ ] **ALB** — Application Load Balancer, health check routing
- [ ] **IAM Roles** — Attach S3 permissions via IAM role (not credentials)

### Long Term

- [ ] **CI/CD Pipeline** — GitHub Actions → ECR → ECS
- [ ] **Metrics & Alarms** — CloudWatch dashboards, alerts
- [ ] **Multi-Region** — S3 cross-region replication

## Learning Outcomes

This project demonstrates competency in:

- **Backend architecture** — Clean separation of concerns, dependency injection
- **FastAPI patterns** — Middleware, exception handling, Pydantic validation
- **Operational readiness** — Structured logging, health checks, containerization
- **Cloud thinking** — Pluggable backends, ALB compatibility, CloudWatch formats
- **Testing at scale** — Integration tests with mocked dependencies

## License

MIT

## Questions?


