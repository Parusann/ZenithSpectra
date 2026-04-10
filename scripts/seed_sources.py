"""Seed the sources table with MVP source list from the spec."""

import asyncio
import uuid
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.database import async_session, engine, Base
from app.models.content import Source, SourceType


MVP_SOURCES = [
    {
        "name": "NASA",
        "source_type": SourceType.AGENCY,
        "base_url": "https://www.nasa.gov",
        "feed_url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "institution": "National Aeronautics and Space Administration",
        "credibility_baseline": 95,
        "region": "United States",
    },
    {
        "name": "ESA",
        "source_type": SourceType.AGENCY,
        "base_url": "https://www.esa.int",
        "feed_url": "https://www.esa.int/rssfeed/Our_Activities/Space_Science",
        "institution": "European Space Agency",
        "credibility_baseline": 95,
        "region": "Europe",
    },
    {
        "name": "arXiv (physics)",
        "source_type": SourceType.PREPRINT,
        "base_url": "https://arxiv.org",
        "feed_url": "https://rss.arxiv.org/rss/physics",
        "institution": "Cornell University",
        "credibility_baseline": 70,
        "region": "United States",
    },
    {
        "name": "Nature",
        "source_type": SourceType.JOURNAL,
        "base_url": "https://www.nature.com",
        "feed_url": "https://www.nature.com/nature.rss",
        "institution": "Springer Nature",
        "credibility_baseline": 95,
        "region": "United Kingdom",
    },
    {
        "name": "Science (AAAS)",
        "source_type": SourceType.JOURNAL,
        "base_url": "https://www.science.org",
        "feed_url": "https://www.science.org/rss/news_current.xml",
        "institution": "American Association for the Advancement of Science",
        "credibility_baseline": 95,
        "region": "United States",
    },
    {
        "name": "Physical Review Letters",
        "source_type": SourceType.JOURNAL,
        "base_url": "https://journals.aps.org/prl",
        "feed_url": "https://journals.aps.org/prl/recent.rss",
        "institution": "American Physical Society",
        "credibility_baseline": 95,
        "region": "United States",
    },
    {
        "name": "Phys.org",
        "source_type": SourceType.SCIENCE_MEDIA,
        "base_url": "https://phys.org",
        "feed_url": "https://phys.org/rss-feed/physics-news/",
        "institution": None,
        "credibility_baseline": 65,
        "region": "United States",
    },
    {
        "name": "Space.com",
        "source_type": SourceType.SCIENCE_MEDIA,
        "base_url": "https://www.space.com",
        "feed_url": "https://www.space.com/feeds/all",
        "institution": None,
        "credibility_baseline": 60,
        "region": "United States",
    },
    {
        "name": "CERN",
        "source_type": SourceType.RESEARCH_INSTITUTION,
        "base_url": "https://home.cern",
        "feed_url": "https://home.cern/api/news/news/feed.rss",
        "institution": "European Organization for Nuclear Research",
        "credibility_baseline": 92,
        "region": "Switzerland",
    },
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        for src_data in MVP_SOURCES:
            source = Source(id=uuid.uuid4(), **src_data)
            session.add(source)
        await session.commit()
        print(f"Seeded {len(MVP_SOURCES)} sources.")


if __name__ == "__main__":
    asyncio.run(seed())
