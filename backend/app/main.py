import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.v1 import router as api_v1_router
from app.ingestion.scheduler import (
    start_scheduler,
    stop_scheduler,
    run_pipeline_guarded,
    ingestion_in_progress,
)
from app.llm.provider import get_llm_provider

logger = logging.getLogger(__name__)

# Keep references to detached background tasks so they are not garbage-collected.
_background_tasks: set[asyncio.Task] = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    stop_scheduler()
    # Release the pooled LLM HTTP client if one was ever created.
    if get_llm_provider.cache_info().currsize:
        await get_llm_provider().aclose()


app = FastAPI(
    title=settings.app_name,
    description="AI-powered science intelligence platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "service": settings.app_name}


async def _run_ingestion_background():
    try:
        stats = await run_pipeline_guarded()
        logger.info("Manual ingestion complete: %s", stats)
    except Exception:
        logger.exception("Manual ingestion failed")


@app.post("/api/v1/ingest")
async def trigger_ingestion():
    """Trigger the ingestion pipeline in the background (non-blocking).

    Returns 202 immediately, or 409 if a run is already in progress.
    """
    if ingestion_in_progress():
        return JSONResponse(status_code=409, content={"status": "already_running"})
    task = asyncio.create_task(_run_ingestion_background())
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)
    return JSONResponse(status_code=202, content={"status": "accepted"})
