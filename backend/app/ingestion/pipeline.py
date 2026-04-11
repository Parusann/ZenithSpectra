"""Ingestion pipeline: fetch, deduplicate, parse, classify, store."""

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.content import Source, ContentItem
from app.ingestion.fetcher import fetch_feed
from app.ingestion.parser import clean_content
from app.ingestion.classifier import classify_category

logger = logging.getLogger(__name__)


async def get_existing_urls(session: AsyncSession) -> set[str]:
    """Load all existing original_urls for deduplication."""
    result = await session.execute(select(ContentItem.original_url))
    return {row[0] for row in result.all()}


async def run_pipeline() -> dict:
    """Run the full ingestion pipeline across all active sources.

    Returns a summary dict with counts of processed/skipped/failed items.
    """
    stats = {"sources": 0, "fetched": 0, "new": 0, "skipped": 0, "errors": 0}
    start = datetime.now(timezone.utc)

    async with async_session() as session:
        # Get all active sources
        result = await session.execute(
            select(Source).where(Source.is_active == True)  # noqa: E712
        )
        sources = result.scalars().all()
        stats["sources"] = len(sources)

        # Load existing URLs for dedup
        existing_urls = await get_existing_urls(session)

        for source in sources:
            if not source.feed_url:
                logger.warning("Source %s has no feed URL, skipping", source.name)
                continue

            entries = await fetch_feed(source.feed_url, source.name)
            stats["fetched"] += len(entries)

            for entry in entries:
                # Deduplicate by URL
                if entry.url in existing_urls:
                    stats["skipped"] += 1
                    continue

                try:
                    cleaned = clean_content(entry.raw_content)
                    category = classify_category(entry.title, cleaned)

                    item = ContentItem(
                        title=entry.title,
                        original_url=entry.url,
                        source_id=source.id,
                        author=entry.author,
                        published_at=entry.published_at,
                        category=category,
                        raw_content=entry.raw_content,
                        cleaned_content=cleaned,
                        credibility_score=source.credibility_baseline,
                        credibility_explanation=(
                            f"Baseline score from {source.name} ({source.source_type.value})"
                        ),
                    )
                    session.add(item)
                    existing_urls.add(entry.url)
                    stats["new"] += 1
                except Exception:
                    logger.exception("Error processing entry: %s", entry.url)
                    stats["errors"] += 1

            # Update last_polled_at
            source.last_polled_at = datetime.now(timezone.utc)

        await session.commit()

    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    logger.info(
        "Pipeline complete in %.1fs: %d sources, %d fetched, %d new, %d skipped, %d errors",
        elapsed, stats["sources"], stats["fetched"], stats["new"],
        stats["skipped"], stats["errors"],
    )
    return stats
