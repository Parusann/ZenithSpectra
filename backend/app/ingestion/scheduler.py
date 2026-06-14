"""APScheduler setup for background ingestion jobs."""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings
from app.ingestion.pipeline import run_pipeline

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# Single-flight lock so manual (/ingest) and scheduled runs never overlap.
_ingestion_lock = asyncio.Lock()


def ingestion_in_progress() -> bool:
    """True if an ingestion run currently holds the single-flight lock."""
    return _ingestion_lock.locked()


async def run_pipeline_guarded() -> dict:
    """Run the ingestion pipeline under a single-flight lock.

    Returns the pipeline stats, or {"status": "already_running"} if a run is
    already in progress.
    """
    if _ingestion_lock.locked():
        logger.info("Ingestion already in progress; skipping run")
        return {"status": "already_running"}
    async with _ingestion_lock:
        return await run_pipeline()


async def scheduled_ingestion():
    """Wrapper for the ingestion pipeline called by APScheduler."""
    logger.info("Starting scheduled ingestion run...")
    try:
        stats = await run_pipeline_guarded()
        logger.info("Scheduled ingestion complete: %s", stats)
    except Exception:
        logger.exception("Scheduled ingestion failed")


def start_scheduler():
    """Start the background scheduler with the ingestion job."""
    scheduler.add_job(
        scheduled_ingestion,
        "interval",
        hours=settings.ingestion_interval_hours,
        id="ingestion_pipeline",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "Scheduler started: ingestion every %d hours",
        settings.ingestion_interval_hours,
    )


def stop_scheduler():
    """Shut down the scheduler gracefully."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")
