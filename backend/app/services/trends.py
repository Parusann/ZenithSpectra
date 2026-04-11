"""Trend calculation engine.

Extracts trending topics from recent content items by analyzing
tag frequency, mention velocity, and recency.
"""

import logging
from collections import Counter
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.content import ContentItem, TrendingTopic, Category

logger = logging.getLogger(__name__)

# Common words to exclude from trending
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "that", "this", "was", "are",
    "be", "has", "have", "had", "not", "new", "will", "can", "may", "how",
    "what", "when", "where", "who", "why", "all", "each", "every", "both",
    "few", "more", "most", "other", "some", "such", "than", "too", "very",
    "just", "about", "also", "after", "before", "could", "would", "should",
    "say", "says", "said", "its", "into", "over", "first", "been", "their",
    "them", "they", "these", "those", "then", "there", "here", "which",
    "one", "two", "three", "many", "much", "like", "get", "got", "make",
    "made", "know", "take", "see", "come", "think", "look", "want", "give",
    "use", "find", "tell", "work", "call", "try", "need", "feel", "become",
    "leave", "put", "mean", "keep", "let", "begin", "show", "hear", "play",
    "run", "move", "live", "believe", "hold", "bring", "happen", "write",
    "provide", "sit", "stand", "lose", "pay", "meet", "include", "continue",
    "set", "learn", "change", "lead", "understand", "watch", "follow",
    "stop", "create", "speak", "read", "allow", "add", "spend", "grow",
    "open", "walk", "win", "offer", "remember", "love", "consider", "appear",
    "buy", "wait", "serve", "die", "send", "expect", "build", "stay",
    "fall", "cut", "reach", "kill", "remain", "suggest", "raise", "pass",
}


def extract_topics_from_title(title: str) -> list[str]:
    """Extract meaningful multi-word and single-word topics from a title."""
    import re

    title_lower = title.lower()
    topics = []

    # Known multi-word phrases to detect
    known_phrases = [
        "black hole", "dark matter", "dark energy", "quantum computing",
        "james webb", "space station", "solar system", "gravitational wave",
        "string theory", "standard model", "big bang", "neutron star",
        "time travel", "warp drive", "quantum entanglement", "error correction",
        "mars rover", "artemis ii", "artemis 2", "quantum gravity",
    ]
    for phrase in known_phrases:
        if phrase in title_lower:
            topics.append(phrase)

    # Single significant words (proper nouns, scientific terms)
    words = re.findall(r"[A-Za-z][a-z]{2,}", title)
    for word in words:
        w = word.lower()
        if w not in STOP_WORDS and len(w) > 3:
            topics.append(w)

    return topics


async def calculate_trends() -> int:
    """Recalculate trending topics from recent content items.

    Returns the number of trending topics updated.
    """
    now = datetime.now(timezone.utc)
    day_ago = now - timedelta(hours=24)
    week_ago = now - timedelta(days=7)

    async with async_session() as session:
        # Get items from the last 7 days
        result = await session.execute(
            select(ContentItem)
            .where(ContentItem.is_active == True)  # noqa: E712
            .where(ContentItem.ingested_at >= week_ago)
        )
        recent_items = result.scalars().all()

        if not recent_items:
            logger.info("No recent items found for trend calculation")
            return 0

        # Count topic mentions in 24h and 7d windows
        mentions_24h: Counter[str] = Counter()
        mentions_7d: Counter[str] = Counter()
        topic_categories: dict[str, Counter[str]] = {}
        topic_item_ids: dict[str, list] = {}

        for item in recent_items:
            topics = extract_topics_from_title(item.title)
            is_recent = item.ingested_at >= day_ago if item.ingested_at else False

            for topic in topics:
                mentions_7d[topic] += 1
                if is_recent:
                    mentions_24h[topic] += 1

                # Track category association
                if topic not in topic_categories:
                    topic_categories[topic] = Counter()
                topic_categories[topic][item.category.value] += 1

                # Track related items
                if topic not in topic_item_ids:
                    topic_item_ids[topic] = []
                topic_item_ids[topic].append(item.id)

        # Filter to topics with at least 2 mentions
        significant = Counter({t: c for t, c in mentions_7d.items() if c >= 2})

        if not significant:
            logger.info("No significant trending topics found")
            return 0

        # Clear existing trends and rebuild
        await session.execute(
            select(TrendingTopic).execution_options(synchronize_session="fetch")
        )
        existing = (await session.execute(select(TrendingTopic))).scalars().all()
        for t in existing:
            await session.delete(t)

        # Create new trending topics
        count = 0
        for topic, mention_7d in significant.most_common(50):
            mention_24h = mentions_24h.get(topic, 0)
            # Velocity: ratio of 24h mentions to 7d average daily rate
            avg_daily = mention_7d / 7
            velocity = (mention_24h / avg_daily) if avg_daily > 0 else 0
            trend_score = mention_7d * (1 + velocity)

            # Determine primary category
            cat_counter = topic_categories.get(topic, Counter())
            primary_cat = cat_counter.most_common(1)[0][0] if cat_counter else "space"

            trending = TrendingTopic(
                name=topic.title(),
                category=Category(primary_cat),
                trend_score=trend_score,
                mention_count_24h=mention_24h,
                mention_count_7d=mention_7d,
                velocity=round(velocity, 2),
                related_item_ids=topic_item_ids.get(topic, [])[:10],
            )
            session.add(trending)
            count += 1

        await session.commit()
        logger.info("Updated %d trending topics", count)
        return count
