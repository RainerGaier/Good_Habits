"""API routes."""

from fastapi import APIRouter

from app.api.absences import router as absences_router
from app.api.completions import router as completions_router
from app.api.habits import router as habits_router

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root API endpoint."""
    return {"message": "Prd_Twin API"}


# Include routers
router.include_router(habits_router)
router.include_router(completions_router)
router.include_router(absences_router)
