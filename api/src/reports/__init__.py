from fastapi import APIRouter

from .average import router as average
from .random import router as random
from .most_events import router as most_events
from .most_feedback import router as most_feedback
from .latest_events import router as latest_events

router = APIRouter()

router.include_router(average, prefix="/average", tags=["average"])
router.include_router(random, prefix="/random", tags=["random"])
router.include_router(most_events, prefix="/most_events", tags=["most_events"])
router.include_router(most_feedback, prefix="/most_feedback", tags=["most_feedback"])
router.include_router(latest_events, prefix="/latest_events", tags=["latest_events"])
