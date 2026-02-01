"""Habit SQLAlchemy model."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.absence import Absence
    from app.models.completion import Completion


class Habit(UUIDMixin, TimestampMixin, Base):
    """SQLAlchemy model for habits."""

    __tablename__ = "habits"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    completions: Mapped[list["Completion"]] = relationship(
        "Completion",
        back_populates="habit",
        cascade="all, delete-orphan",
    )

    absences: Mapped[list["Absence"]] = relationship(
        "Absence",
        back_populates="habit",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        """Return string representation of Habit."""
        return f"<Habit(id={self.id}, name={self.name})>"
