"""Completion tracking API endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.completion import (
    CompletionCreate,
    CompletionResponse,
    CompletionsListResponse,
)
from app.services.habit_service import HabitService

router = APIRouter(prefix="/habits", tags=["completions"])


@router.post(
    "/{habit_id}/complete",
    response_model=CompletionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def complete_habit(
    habit_id: str,
    completion_data: CompletionCreate | None = None,
    db: AsyncSession = Depends(get_db),
) -> CompletionResponse:
    """Mark a habit as complete for a date (defaults to today)."""
    service = HabitService(db)

    completion_date = None
    if completion_data and completion_data.date:
        completion_date = completion_data.date

    completion = await service.complete_habit(habit_id, completion_date)
    if not completion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )
    return CompletionResponse(
        habit_id=completion.habit_id,
        date=completion.completed_date,
        completed=True,
    )


@router.get("/{habit_id}/completions", response_model=CompletionsListResponse)
async def get_completions(
    habit_id: str,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> CompletionsListResponse:
    """Get completion history for a habit."""
    service = HabitService(db)

    # Verify habit exists
    habit = await service.get_habit(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    completions = await service.get_completions(habit_id, start_date, end_date)
    return CompletionsListResponse(habit_id=habit_id, completions=completions)


@router.delete(
    "/{habit_id}/completions/{completion_date}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_completion(
    habit_id: str,
    completion_date: date,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove a completion for a specific date (undo)."""
    service = HabitService(db)

    # Verify habit exists
    habit = await service.get_habit(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    deleted = await service.delete_completion(habit_id, completion_date)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completion not found",
        )
