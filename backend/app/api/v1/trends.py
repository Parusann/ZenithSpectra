"""Trends API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.content import TrendingTopic
from app.api.v1.schemas import TrendingTopicResponse

router = APIRouter(prefix="/trends", tags=["trends"])


@router.get("", response_model=list[TrendingTopicResponse])
async def list_trends(
    category: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Get current trending topics sorted by velocity."""
    query = select(TrendingTopic).order_by(desc(TrendingTopic.velocity))

    if category:
        query = query.where(TrendingTopic.category == category.upper())

    query = query.limit(limit)
    result = await db.execute(query)
    topics = result.scalars().all()

    return [TrendingTopicResponse.model_validate(t) for t in topics]
