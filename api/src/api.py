from fastapi import APIRouter

from .namespaces import router as namespaces
from .actor import router as actors
from .items import router as items
from .events import router as events
from .feedbacks import router as feedbacks

from .experiments import router as experiments

router = APIRouter()

router.include_router(namespaces, prefix="/namespaces", tags=["namespaces"])
router.include_router(actors, prefix="/actors", tags=["users"])
router.include_router(items, prefix="/items", tags=["items"])
router.include_router(events, prefix="/events", tags=["events"])
router.include_router(feedbacks, prefix="/feedbacks", tags=["feedbacks"])

router.include_router(experiments, prefix="/experiments", tags=["experiments"])
