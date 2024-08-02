from fastapi import APIRouter

from .namespaces import router as namespaces
from .actors import router as actors
from .items import router as items
from .events import router as events
from .feedbacks import router as feedbacks

from .reports import router as reports
from .stats import router as stats

router = APIRouter()

router.include_router(namespaces, prefix="/namespaces", tags=["namespaces"])

# return resources from all namespaces
router.include_router(actors, prefix="/actors", tags=["actors"])
router.include_router(items, prefix="/items", tags=["items"])
router.include_router(events, prefix="/events", tags=["events"])
router.include_router(feedbacks, prefix="/feedbacks", tags=["feedbacks"])
router.include_router(stats, prefix="/stats", tags=["stats"])

router.include_router(
    actors, prefix="/namespace/{namespace_name}/actors", tags=["actors"]
)
router.include_router(items, prefix="/namespace/{namespace_name}/items", tags=["items"])
router.include_router(
    events, prefix="/namespace/{namespace_name}/events", tags=["events"]
)
router.include_router(
    feedbacks, prefix="/namespace/{namespace_name}/feedbacks", tags=["feedbacks"]
)
router.include_router(stats, prefix="/namespace/{namespace_name}/stats", tags=["stats"])

# reports
router.include_router(
    reports, prefix="/namespace/{namespace_name}/reports", tags=["reports"]
)
