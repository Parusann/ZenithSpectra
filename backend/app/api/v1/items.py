"""Content items API endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.content import ContentItem, Source
from app.api.v1.schemas import (
    ContentItemSummary,
    ContentItemDetail,
    PaginatedResponse,
    QARequest,
    QAResponse,
)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=PaginatedResponse)
async def list_items(
    category: str | None = None,
    source_type: str | None = None,
    credibility_min: int | None = None,
    scientific_status: str | None = None,
    sort: str = "newest",
    limit: int = Query(default=20, le=100),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List content items with filtering, sorting, and pagination."""
    query = select(ContentItem).options(selectinload(ContentItem.source))
    count_query = select(func.count(ContentItem.id))

    # Apply filters
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

    # Apply filter for active items only
    query = query.where(ContentItem.is_active == True)  # noqa: E712
    count_query = count_query.where(ContentItem.is_active == True)  # noqa: E712

    # Sorting
    if sort == "trending":
        query = query.order_by(desc(ContentItem.trend_score))
    elif sort == "credibility":
        query = query.order_by(desc(ContentItem.credibility_score))
    else:  # newest
        query = query.order_by(desc(ContentItem.published_at))

    # Get total count
    total = (await db.execute(count_query)).scalar() or 0

    # Paginate
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()

    return PaginatedResponse(
        items=[ContentItemSummary.model_validate(item) for item in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{item_id}", response_model=ContentItemDetail)
async def get_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get a single content item with full detail."""
    result = await db.execute(
        select(ContentItem)
        .options(selectinload(ContentItem.source))
        .where(ContentItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ContentItemDetail.model_validate(item)


@router.post("/{item_id}/ask", response_model=QAResponse)
async def ask_question(
    item_id: UUID,
    body: QARequest,
    db: AsyncSession = Depends(get_db),
):
    """Ask a question about a specific content item."""
    from app.llm.service import answer_question
    from app.models.content import QAInteraction

    result = await db.execute(
        select(ContentItem).where(ContentItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    context = item.cleaned_content or item.raw_content or item.title
    answer = await answer_question(context, body.question)

    # Log interaction
    interaction = QAInteraction(
        item_id=item_id,
        question=body.question,
        answer=answer,
    )
    db.add(interaction)
    await db.commit()

    return QAResponse(question=body.question, answer=answer, item_id=item_id)
