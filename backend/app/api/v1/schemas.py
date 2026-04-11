"""Pydantic response schemas for the API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SourceResponse(BaseModel):
    id: UUID
    name: str
    source_type: str
    base_url: str | None
    institution: str | None
    credibility_baseline: int
    region: str | None
    is_active: bool
    last_polled_at: datetime | None

    model_config = {"from_attributes": True}


class ContentItemSummary(BaseModel):
    id: UUID
    title: str
    original_url: str
    author: str | None
    published_at: datetime | None
    ingested_at: datetime
    category: str
    tags: list[str] | None
    summary_quick: str | None
    scientific_status: str | None
    credibility_score: int | None
    credibility_explanation: str | None
    trend_score: float | None
    source: SourceResponse | None

    model_config = {"from_attributes": True}


class ContentItemDetail(ContentItemSummary):
    summary_expanded: str | None
    explanation_beginner: str | None
    explanation_intermediate: str | None
    explanation_technical: str | None
    cleaned_content: str | None
    subcategory: str | None

    model_config = {"from_attributes": True}


class TrendingTopicResponse(BaseModel):
    id: UUID
    name: str
    category: str
    trend_score: float
    mention_count_24h: int
    mention_count_7d: int
    velocity: float
    updated_at: datetime

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    slug: str
    name: str
    description: str
    item_count: int


class QARequest(BaseModel):
    question: str


class QAResponse(BaseModel):
    question: str
    answer: str
    item_id: UUID


class PaginatedResponse(BaseModel):
    items: list[ContentItemSummary]
    total: int
    limit: int
    offset: int
