"""Sources API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.content import Source
from app.api.v1.schemas import SourceResponse

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)):
    """List all tracked sources with credibility info."""
    result = await db.execute(select(Source).order_by(Source.credibility_baseline.desc()))
    sources = result.scalars().all()
    return [SourceResponse.model_validate(s) for s in sources]
