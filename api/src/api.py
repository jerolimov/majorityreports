from fastapi import APIRouter

from .projects import router as projects
from .users import router as users
from .items import router as items
from .events import router as events
from .feedbacks import router as feedbacks

router = APIRouter()

router.include_router(projects, prefix="/projects", tags=["projects"])
router.include_router(users, prefix="/users", tags=["users"])
router.include_router(items, prefix="/items", tags=["items"])
router.include_router(events, prefix="/events", tags=["events"])
router.include_router(feedbacks, prefix="/feedbacks", tags=["feedbacks"])
