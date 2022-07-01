from fastapi import APIRouter

from .frames import router as frames_router

router = APIRouter()
router.include_router(frames_router)
