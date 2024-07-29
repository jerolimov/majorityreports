from fastapi import APIRouter

from .random import router as random

router = APIRouter()

router.include_router(random, prefix="/random", tags=["random"])
