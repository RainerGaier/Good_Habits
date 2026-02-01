"""Absence tracking API endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.absence import (
    AbsenceCreate,
    AbsenceItem,
    AbsenceResponse,
    AbsencesListResponse,
)
from app.services.habit_service import HabitService

router = APIRouter(prefix="/habits", tags=["absences"])


@router.post(
    "/{habit_id}/absences",
    response_model=AbsenceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_absence(
    habit_id: str,
    absence_data: AbsenceCreate | None = None,
    db: AsyncSession = Depends(get_db),
) -> AbsenceResponse:
    """Mark a planned absence for a habit (defaults to today)."""
    service = HabitService(db)

    absence_date = None
    reason = None
    if absence_data:
        absence_date = absence_data.date
        reason = absence_data.reason

    absence = await service.create_absence(habit_id, absence_date, reason)
    if not absence:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )
    return AbsenceResponse(
        habit_id=absence.habit_id,
        date=absence.absence_date,
        reason=absence.reason,
    )


@router.get("/{habit_id}/absences", response_model=AbsencesListResponse)
async def get_absences(
    habit_id: str,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
) -> AbsencesListResponse:
    """Get absence history for a habit."""
    service = HabitService(db)

    # Verify habit exists
    habit = await service.get_habit(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    absences = await service.get_absences(habit_id, start_date, end_date)
    return AbsencesListResponse(
        habit_id=habit_id,
        absences=[AbsenceItem(date=d, reason=r) for d, r in absences],
    )


@router.delete(
    "/{habit_id}/absences/{absence_date}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_absence(
    habit_id: str,
    absence_date: date,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove a planned absence for a specific date."""
    service = HabitService(db)

    # Verify habit exists
    habit = await service.get_habit(habit_id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found",
        )

    deleted = await service.delete_absence(habit_id, absence_date)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Absence not found",
        )
