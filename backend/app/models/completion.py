"""Completion SQLAlchemy model."""

from datetime import UTC, date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.habit import Habit


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class Completion(Base):
    """SQLAlchemy model for habit completions."""

    __tablename__ = "completions"
    __table_args__ = (
        UniqueConstraint("habit_id", "completed_date", name="uq_habit_date"),
        Index("idx_completions_habit_date", "habit_id", "completed_date"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    habit_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("habits.id", ondelete="CASCADE"),
        nullable=False,
    )
    completed_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)

    habit: Mapped["Habit"] = relationship("Habit", back_populates="completions")

    def __repr__(self) -> str:
        """Return string representation of Completion."""
        return f"<Completion(habit_id={self.habit_id}, date={self.completed_date})>"
