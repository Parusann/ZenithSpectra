"""Ingestion pipeline: fetch, deduplicate, parse, classify, store."""

import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import async_session
from app.models.content import Source, ContentItem, Category, ScientificStatus
from app.ingestion.fetcher import fetch_feed
from app.ingestion.parser import clean_content
from app.ingestion.classifier import classify_category
from app.services.credibility import score_credibility
from app.services.trends import calculate_trends
from app.llm.service import generate_summary, classify_content, evaluate_credibility

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

                    cred_score, cred_explanation = score_credibility(
                        source_baseline=source.credibility_baseline,
                        source_type=source.source_type,
                        original_url=entry.url,
                        title=entry.title,
                        content=cleaned,
                    )

                    # LLM enrichment (optional, gated by config flag)
                    llm_summary = None
                    llm_tags = None
                    llm_status = None
                    llm_cred_adjustment = 0
                    llm_category = None

                    if settings.enable_llm_enrichment:
                        try:
                            llm_summary = await generate_summary(cleaned, "quick")
                        except Exception:
                            logger.warning("LLM summary failed for %s", entry.url)

                        try:
                            classification = await classify_content(cleaned)
                            raw_cat = classification.get("category")
                            raw_status = classification.get("scientific_status")
                            llm_tags = classification.get("tags", [])

                            if raw_cat:
                                try:
                                    llm_category = Category(raw_cat)
                                except ValueError:
                                    llm_category = None

                            if raw_status:
                                try:
                                    llm_status = ScientificStatus(raw_status)
                                except ValueError:
                                    llm_status = None
                        except Exception:
                            logger.warning("LLM classification failed for %s", entry.url)

                        try:
                            cred_result = await evaluate_credibility(cleaned, entry.title)
                            llm_cred_adjustment = cred_result.get("score_adjustment", 0)
                        except Exception:
                            logger.warning("LLM credibility eval failed for %s", entry.url)

                    final_score = max(0, min(100, cred_score + llm_cred_adjustment))

                    item = ContentItem(
                        title=entry.title,
                        original_url=entry.url,
                        source_id=source.id,
                        author=entry.author,
                        published_at=entry.published_at,
                        category=llm_category or category,
                        raw_content=entry.raw_content,
                        cleaned_content=cleaned,
                        credibility_score=final_score,
                        credibility_explanation=cred_explanation,
                        summary_quick=llm_summary,
                        scientific_status=llm_status,
                        tags=llm_tags,
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

    # Update trending topics after ingestion
    try:
        trend_count = await calculate_trends()
        stats["trends_updated"] = trend_count
    except Exception:
        logger.exception("Trend calculation failed")
        stats["trends_updated"] = 0

    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    logger.info(
        "Pipeline complete in %.1fs: %d sources, %d fetched, %d new, %d skipped, %d errors",
        elapsed, stats["sources"], stats["fetched"], stats["new"],
        stats["skipped"], stats["errors"],
    )
    return stats
