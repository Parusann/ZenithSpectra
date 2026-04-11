"""RSS/Atom feed fetcher using feedparser."""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone

import feedparser
import httpx

logger = logging.getLogger(__name__)


@dataclass
class FeedEntry:
    title: str
    url: str
    author: str | None
    published_at: datetime | None
    raw_content: str
    source_name: str


async def fetch_feed(feed_url: str, source_name: str) -> list[FeedEntry]:
    """Fetch and parse an RSS/Atom feed, returning structured entries."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(feed_url, follow_redirects=True)
            response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error("Failed to fetch feed %s (%s): %s", source_name, feed_url, e)
        return []

    feed = feedparser.parse(response.text)

    if feed.bozo and not feed.entries:
        logger.warning("Malformed feed from %s: %s", source_name, feed.bozo_exception)
        return []

    entries = []
    for entry in feed.entries:
        # Extract content — prefer full content, fall back to summary
        content = ""
        if hasattr(entry, "content") and entry.content:
            content = entry.content[0].get("value", "")
        elif hasattr(entry, "summary"):
            content = entry.summary or ""
        elif hasattr(entry, "description"):
            content = entry.description or ""

        # Parse published date
        published = None
        time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
        if time_struct:
            try:
                published = datetime(*time_struct[:6], tzinfo=timezone.utc)
            except (ValueError, TypeError):
                pass

        url = entry.get("link", "")
        title = entry.get("title", "")

        if not url or not title:
            continue

        entries.append(FeedEntry(
            title=title.strip(),
            url=url.strip(),
            author=entry.get("author"),
            published_at=published,
            raw_content=content,
            source_name=source_name,
        ))

    logger.info("Fetched %d entries from %s", len(entries), source_name)
    return entries
