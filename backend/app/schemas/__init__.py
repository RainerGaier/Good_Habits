"""Pydantic schemas for API validation."""

from app.schemas.absence import (
    AbsenceCreate,
    AbsenceItem,
    AbsenceResponse,
    AbsencesListResponse,
)
from app.schemas.completion import (
    CompletionCreate,
    CompletionResponse,
    CompletionsListResponse,
)
from app.schemas.habit import HabitCreate, HabitResponse, HabitUpdate
from app.schemas.stats import CompletionRate, HabitWithStatsResponse

__all__ = [
    "HabitCreate",
    "HabitUpdate",
    "HabitResponse",
    "CompletionCreate",
    "CompletionResponse",
    "CompletionsListResponse",
    "AbsenceCreate",
    "AbsenceResponse",
    "AbsenceItem",
    "AbsencesListResponse",
    "CompletionRate",
    "HabitWithStatsResponse",
]
