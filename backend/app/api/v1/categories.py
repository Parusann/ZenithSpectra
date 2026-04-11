"""Categories API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.content import ContentItem, Category
from app.api.v1.schemas import CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

CATEGORY_META = {
    "space": {
        "name": "Space Exploration",
        "description": "NASA missions, SpaceX, Artemis, Mars rovers, exoplanets, telescopes, satellites, and launch systems.",
    },
    "quantum": {
        "name": "Quantum Physics",
        "description": "Quantum entanglement, quantum computing, error correction, quantum communication, and teleportation experiments.",
    },
    "theoretical": {
        "name": "Theoretical Physics",
        "description": "Black holes, dark matter, dark energy, string theory, quantum gravity, and extra dimensions.",
    },
    "frontier": {
        "name": "Frontier Ideas",
        "description": "Time travel, warp drives, simulation theory, traversable wormholes, and exotic metrics.",
    },
}


@router.get("", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """List all categories with item counts."""
    result = await db.execute(
        select(ContentItem.category, func.count(ContentItem.id))
        .where(ContentItem.is_active == True)  # noqa: E712
        .group_by(ContentItem.category)
    )
    counts = {row[0].value.lower(): row[1] for row in result.all()}

    return [
        CategoryResponse(
            slug=slug,
            name=meta["name"],
            description=meta["description"],
            item_count=counts.get(slug, 0),
        )
        for slug, meta in CATEGORY_META.items()
    ]


@router.get("/{slug}", response_model=CategoryResponse)
async def get_category(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a single category with metadata."""
    if slug not in CATEGORY_META:
        raise HTTPException(status_code=404, detail="Category not found")

    meta = CATEGORY_META[slug]
    result = await db.execute(
        select(func.count(ContentItem.id))
        .where(ContentItem.category == slug.upper())
        .where(ContentItem.is_active == True)  # noqa: E712
    )
    count = result.scalar() or 0

    return CategoryResponse(
        slug=slug, name=meta["name"], description=meta["description"], item_count=count
    )
