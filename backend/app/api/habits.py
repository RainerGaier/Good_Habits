"""Habit CRUD API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from app.schemas.stats import HabitWithStatsResponse
from app.services.habit_service import HabitService
from app.services.stats_service import StatsService

router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("", response_model=list[HabitWithStatsResponse])
async def list_habits(
    db: AsyncSession = Depends(get_db),
) -> list[HabitWithStatsResponse]:
    """Get all habits with computed statistics."""
    service = StatsService(db)
    return await service.get_all_habits_with_stats()


@router.post("", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit_data: HabitCreate,
    db: AsyncSession = Depends(get_db),
) -> HabitResponse:
    """Create a new habit."""
    service = HabitService(db)
    habit = await service.create_habit(habit_data)
    return HabitResponse.model_validate(habit)


@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(
    habit_id: str,
    db: AsyncSession = Depends(get_db),
) -> HabitResponse:
    """Get a specific habit by ID."""
    service = HabitService(db)
    habit = await service.get_habit(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )
    return HabitResponse.model_validate(habit)


@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: str,
    habit_data: HabitUpdate,
    db: AsyncSession = Depends(get_db),
) -> HabitResponse:
    """Update an existing habit."""
    service = HabitService(db)
    habit = await service.update_habit(habit_id, habit_data)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )
    return HabitResponse.model_validate(habit)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: str,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a habit."""
    service = HabitService(db)
    deleted = await service.delete_habit(habit_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )
