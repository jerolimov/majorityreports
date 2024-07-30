from fastapi import APIRouter

from .random import router as random
from .most_events import router as most_events
from .most_feedback import router as most_feedback

router = APIRouter()

router.include_router(random, prefix="/random", tags=["random"])
router.include_router(most_events, prefix="/most_events", tags=["most_feedback"])
router.include_router(most_feedback, prefix="/most_feedback", tags=["most_feedback"])
