"""Search API endpoint with PostgreSQL full-text search."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, desc, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.content import ContentItem, Source
from app.api.v1.schemas import ContentItemSummary, PaginatedResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=PaginatedResponse)
async def search_items(
    q: str = Query(..., min_length=1),
    category: str | None = None,
    source_type: str | None = None,
    credibility_min: int | None = None,
    scientific_status: str | None = None,
    limit: int = Query(default=20, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """Search content items using PostgreSQL full-text search."""
    # Build tsquery from search terms
    ts_query = func.plainto_tsquery("english", q)
    ts_vector = func.to_tsvector(
        "english",
        func.coalesce(ContentItem.title, cast("", String)) + " " +
        func.coalesce(ContentItem.cleaned_content, cast("", String)),
    )

    query = (
        select(ContentItem)
        .options(selectinload(ContentItem.source))
        .where(ts_vector.op("@@")(ts_query))
        .where(ContentItem.is_active == True)  # noqa: E712
    )
    count_query = (
        select(func.count(ContentItem.id))
        .where(ts_vector.op("@@")(ts_query))
        .where(ContentItem.is_active == True)  # noqa: E712
    )

    if category:
        query = query.where(ContentItem.category == category.upper())
        count_query = count_query.where(ContentItem.category == category.upper())
    if source_type:
        query = query.join(Source).where(Source.source_type == source_type.upper())
        count_query = count_query.join(Source).where(Source.source_type == source_type.upper())
    if credibility_min is not None:
        query = query.where(ContentItem.credibility_score >= credibility_min)
        count_query = count_query.where(ContentItem.credibility_score >= credibility_min)
    if scientific_status:
        query = query.where(ContentItem.scientific_status == scientific_status.upper())
        count_query = count_query.where(ContentItem.scientific_status == scientific_status.upper())

    # Rank by relevance
    rank = func.ts_rank(ts_vector, ts_query)
    query = query.order_by(desc(rank))

    total = (await db.execute(count_query)).scalar() or 0
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=[ContentItemSummary.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )
