"""Pydantic schemas for statistics responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompletionRate(BaseModel):
    """Completion rate statistics."""

    week: float
    month: float
    all_time: float


class HabitWithStatsResponse(BaseModel):
    """Schema for habit response with computed statistics."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
    current_streak: int
    best_streak: int
    completion_rate: CompletionRate
    completed_today: bool
