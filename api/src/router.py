from fastapi import APIRouter

from .namespaces.crud import router as namespaces_crud
from .namespaces.query import router as namespaces_query
from .actors.crud import router as actors_crud
from .actors.query import router as actors_query
from .items.crud import router as items_crud
from .items.query import router as items_query
from .events.crud import router as events_crud
from .events.query import router as events_query
from .feedbacks.crud import router as feedbacks_crud
from .feedbacks.query import router as feedbacks_query

from .stats.stats import router as stats

from .reports import router as reports

router = APIRouter()

router.include_router(namespaces_crud, prefix="/namespaces", tags=["namespaces"])
router.include_router(namespaces_query, prefix="/namespaces", tags=["namespaces"])

# return resources from all namespaces
router.include_router(actors_query, prefix="/actors", tags=["actors"])
router.include_router(items_query, prefix="/items", tags=["items"])
router.include_router(events_query, prefix="/events", tags=["events"])
router.include_router(feedbacks_query, prefix="/feedbacks", tags=["feedbacks"])

router.include_router(stats, prefix="/stats", tags=["stats"])

router.include_router(
    actors_crud, prefix="/namespaces/{namespace_name}/actors", tags=["actors"]
)
router.include_router(
    actors_query, prefix="/namespaces/{namespace_name}/actors", tags=["actors"]
)
router.include_router(
    items_crud, prefix="/namespaces/{namespace_name}/items", tags=["items"]
)
router.include_router(
    items_query, prefix="/namespaces/{namespace_name}/items", tags=["items"]
)
router.include_router(
    events_crud, prefix="/namespaces/{namespace_name}/events", tags=["events"]
)
router.include_router(
    events_query, prefix="/namespaces/{namespace_name}/events", tags=["events"]
)
router.include_router(
    feedbacks_crud, prefix="/namespaces/{namespace_name}/feedbacks", tags=["feedbacks"]
)
router.include_router(
    feedbacks_query, prefix="/namespaces/{namespace_name}/feedbacks", tags=["feedbacks"]
)

router.include_router(
    stats, prefix="/namespaces/{namespace_name}/stats", tags=["stats"]
)

# reports
router.include_router(
    reports, prefix="/namespaces/{namespace_name}/reports", tags=["reports"]
)
