"""Pydantic schemas for Absence operations."""

from datetime import date as date_type

from pydantic import BaseModel, ConfigDict, Field


class AbsenceCreate(BaseModel):
    """Schema for creating an absence."""

    date: date_type | None = Field(
        None, description="Date to mark as absence. Defaults to today."
    )
    reason: str | None = Field(None, max_length=100, description="Reason for absence.")


class AbsenceResponse(BaseModel):
    """Schema for absence response."""

    model_config = ConfigDict(from_attributes=True)

    habit_id: str
    date: date_type
    reason: str | None = None


class AbsenceItem(BaseModel):
    """Schema for a single absence in list."""

    date: date_type
    reason: str | None = None


class AbsencesListResponse(BaseModel):
    """Schema for listing absences."""

    habit_id: str
    absences: list[AbsenceItem]
