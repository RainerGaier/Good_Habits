"""Pydantic schemas for Habit operations."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HabitCreate(BaseModel):
    """Schema for creating a new habit."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class HabitUpdate(BaseModel):
    """Schema for updating an existing habit."""

    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class HabitResponse(BaseModel):
    """Schema for habit response."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
