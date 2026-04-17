# ── Stage 1: Builder ──────────────────────────────────────
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-dev

# ── Stage 2: Runtime ──────────────────────────────────────
FROM python:3.13-slim AS runtime

WORKDIR /app

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Copy virtual environment from builder
COPY --from=builder /app/.venv ./.venv

# Copy application code
COPY app/ ./app/

# Give appuser ownership
RUN chown -R appuser:appuser /app

USER appuser

# Make uploads directory
RUN mkdir -p /app/uploads

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]