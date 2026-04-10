import uuid
import enum
from datetime import datetime

from sqlalchemy import String, Text, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Category(str, enum.Enum):
    SPACE = "space"
    QUANTUM = "quantum"
    THEORETICAL = "theoretical"
    FRONTIER = "frontier"


class SourceType(str, enum.Enum):
    AGENCY = "agency"
    RESEARCH_INSTITUTION = "research_institution"
    JOURNAL = "journal"
    PREPRINT = "preprint"
    SCIENCE_MEDIA = "science_media"
    GENERAL_NEWS = "general_news"


class ScientificStatus(str, enum.Enum):
    ESTABLISHED = "established"
    SUPPORTED = "supported"
    ACTIVE_RESEARCH = "active_research"
    SPECULATIVE = "speculative"
    HIGHLY_SPECULATIVE = "highly_speculative"
    MEDIA_HYPE = "media_hype"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    base_url: Mapped[str | None] = mapped_column(Text)
    feed_url: Mapped[str | None] = mapped_column(Text)
    institution: Mapped[str | None] = mapped_column(Text)
    credibility_baseline: Mapped[int] = mapped_column(Integer, default=50)
    region: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_polled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    poll_interval_minutes: Mapped[int] = mapped_column(Integer, default=360)

    items: Mapped[list["ContentItem"]] = relationship(back_populates="source")


class ContentItem(Base):
    __tablename__ = "content_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    original_url: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sources.id"))
    author: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    category: Mapped[Category] = mapped_column(Enum(Category), nullable=False)
    subcategory: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    summary_quick: Mapped[str | None] = mapped_column(Text)
    summary_expanded: Mapped[str | None] = mapped_column(Text)
    explanation_beginner: Mapped[str | None] = mapped_column(Text)
    explanation_intermediate: Mapped[str | None] = mapped_column(Text)
    explanation_technical: Mapped[str | None] = mapped_column(Text)
    scientific_status: Mapped[ScientificStatus | None] = mapped_column(Enum(ScientificStatus))
    credibility_score: Mapped[int | None] = mapped_column(Integer)
    credibility_explanation: Mapped[str | None] = mapped_column(Text)
    trend_score: Mapped[float | None] = mapped_column(Float)
    raw_content: Mapped[str | None] = mapped_column(Text)
    cleaned_content: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    source: Mapped["Source"] = relationship(back_populates="items")
    qa_interactions: Mapped[list["QAInteraction"]] = relationship(back_populates="item")


class TrendingTopic(Base):
    __tablename__ = "trending_topics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[Category] = mapped_column(Enum(Category))
    trend_score: Mapped[float] = mapped_column(Float, default=0.0)
    mention_count_24h: Mapped[int] = mapped_column(Integer, default=0)
    mention_count_7d: Mapped[int] = mapped_column(Integer, default=0)
    velocity: Mapped[float] = mapped_column(Float, default=0.0)
    related_item_ids: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(UUID(as_uuid=True)))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class QAInteraction(Base):
    __tablename__ = "qa_interactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("content_items.id"))
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    item: Mapped["ContentItem"] = relationship(back_populates="qa_interactions")
