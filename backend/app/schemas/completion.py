"""Pydantic schemas for Completion operations."""

from datetime import date as date_type

from pydantic import BaseModel, ConfigDict, Field


class CompletionCreate(BaseModel):
    """Schema for creating a completion."""

    date: date_type | None = Field(
        None, description="Date to mark as complete. Defaults to today."
    )


class CompletionResponse(BaseModel):
    """Schema for completion response."""

    model_config = ConfigDict(from_attributes=True)

    habit_id: str
    date: date_type
    completed: bool = True


class CompletionsListResponse(BaseModel):
    """Schema for listing completions."""

    habit_id: str
    completions: list[date_type]
