from fastapi import APIRouter

from app.api.v1.items import router as items_router
from app.api.v1.categories import router as categories_router
from app.api.v1.trends import router as trends_router
from app.api.v1.sources import router as sources_router
from app.api.v1.search import router as search_router

router = APIRouter()
router.include_router(items_router)
router.include_router(categories_router)
router.include_router(trends_router)
router.include_router(sources_router)
router.include_router(search_router)
