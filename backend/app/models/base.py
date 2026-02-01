"""Base model mixins for SQLAlchemy models."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class UUIDMixin:
    """Mixin providing UUID primary key."""

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


class TimestampMixin:
    """Mixin providing created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now,
        onupdate=utc_now,
    )
