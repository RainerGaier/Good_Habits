"""Absence SQLAlchemy model."""

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


class Absence(Base):
    """SQLAlchemy model for planned absences."""

    __tablename__ = "absences"
    __table_args__ = (
        UniqueConstraint("habit_id", "absence_date", name="uq_habit_absence_date"),
        Index("idx_absences_habit_date", "habit_id", "absence_date"),
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
    absence_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)

    habit: Mapped["Habit"] = relationship("Habit", back_populates="absences")

    def __repr__(self) -> str:
        """Return string representation of Absence."""
        return f"<Absence(habit_id={self.habit_id}, date={self.absence_date})>"
