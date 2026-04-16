from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import get_logger
from app.storage.local import LocalStorage

logger = get_logger("lifespan")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── STARTUP ──────────────────────────────────────────────
    logger.info(f"accessflow.startup env={settings.app_name} storage={settings.storage_backend}")

    storage = LocalStorage(settings.storage_path)
    storage.ensure_directory()

    logger.info("accessflow.startup.complete")

    yield

    # ── SHUTDOWN ─────────────────────────────────────────────
    logger.info("accessflow.shutdown")