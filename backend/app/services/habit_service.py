"""Habit, Completion, and Absence service layer."""

import uuid
from datetime import date

import structlog
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.absence import Absence
from app.models.completion import Completion
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate

logger = structlog.get_logger()


class HabitService:
    """Service for Habit, Completion, and Absence CRUD operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize service with database session."""
        self.session = session

    async def create_habit(self, habit_data: HabitCreate) -> Habit:
        """Create a new habit."""
        habit = Habit(
            name=habit_data.name,
            description=habit_data.description,
        )
        self.session.add(habit)
        await self.session.commit()
        await self.session.refresh(habit)
        logger.info("habit_created", habit_id=habit.id, name=habit.name)
        return habit

    async def get_habit(self, habit_id: str) -> Habit | None:
        """Get a habit by ID."""
        result = await self.session.execute(select(Habit).where(Habit.id == habit_id))
        return result.scalar_one_or_none()

    async def get_all_habits(self) -> list[Habit]:
        """Get all habits."""
        result = await self.session.execute(select(Habit))
        return list(result.scalars().all())

    async def update_habit(
        self, habit_id: str, habit_data: HabitUpdate
    ) -> Habit | None:
        """Update an existing habit."""
        habit = await self.get_habit(habit_id)
        if not habit:
            return None

        if habit_data.name is not None:
            habit.name = habit_data.name
        if habit_data.description is not None:
            habit.description = habit_data.description

        await self.session.commit()
        await self.session.refresh(habit)
        logger.info("habit_updated", habit_id=habit.id)
        return habit

    async def delete_habit(self, habit_id: str) -> bool:
        """Delete a habit by ID."""
        habit = await self.get_habit(habit_id)
        if not habit:
            return False

        await self.session.delete(habit)
        await self.session.commit()
        logger.info("habit_deleted", habit_id=habit_id)
        return True

    # Completion methods

    async def complete_habit(
        self, habit_id: str, completion_date: date | None = None
    ) -> Completion | None:
        """Mark a habit as complete for a date.

        Returns existing completion if already completed (idempotent).
        Returns None if habit doesn't exist.
        """
        habit = await self.get_habit(habit_id)
        if not habit:
            return None

        if completion_date is None:
            completion_date = date.today()

        # Check for existing completion
        existing = await self.get_completion(habit_id, completion_date)
        if existing:
            logger.info(
                "completion_already_exists",
                habit_id=habit_id,
                date=str(completion_date),
            )
            return existing

        completion = Completion(
            id=str(uuid.uuid4()),
            habit_id=habit_id,
            completed_date=completion_date,
        )

        try:
            self.session.add(completion)
            await self.session.commit()
            await self.session.refresh(completion)
            logger.info(
                "habit_completed",
                habit_id=habit_id,
                date=str(completion_date),
            )
            return completion
        except IntegrityError:
            await self.session.rollback()
            # Race condition - completion was added by another request
            return await self.get_completion(habit_id, completion_date)

    async def get_completion(
        self, habit_id: str, completion_date: date
    ) -> Completion | None:
        """Get a specific completion."""
        result = await self.session.execute(
            select(Completion).where(
                Completion.habit_id == habit_id,
                Completion.completed_date == completion_date,
            )
        )
        return result.scalar_one_or_none()

    async def delete_completion(self, habit_id: str, completion_date: date) -> bool:
        """Delete a completion (undo)."""
        completion = await self.get_completion(habit_id, completion_date)
        if not completion:
            return False

        await self.session.delete(completion)
        await self.session.commit()
        logger.info(
            "completion_deleted",
            habit_id=habit_id,
            date=str(completion_date),
        )
        return True

    async def get_completions(
        self,
        habit_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[date]:
        """Get completion dates for a habit within a date range."""
        query = select(Completion.completed_date).where(Completion.habit_id == habit_id)

        if start_date:
            query = query.where(Completion.completed_date >= start_date)
        if end_date:
            query = query.where(Completion.completed_date <= end_date)

        query = query.order_by(Completion.completed_date)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    # Absence methods

    async def create_absence(
        self,
        habit_id: str,
        absence_date: date | None = None,
        reason: str | None = None,
    ) -> Absence | None:
        """Mark a planned absence for a habit.

        Returns existing absence if already marked (idempotent).
        Returns None if habit doesn't exist.
        """
        habit = await self.get_habit(habit_id)
        if not habit:
            return None

        if absence_date is None:
            absence_date = date.today()

        # Check for existing absence
        existing = await self.get_absence(habit_id, absence_date)
        if existing:
            logger.info(
                "absence_already_exists",
                habit_id=habit_id,
                date=str(absence_date),
            )
            return existing

        absence = Absence(
            id=str(uuid.uuid4()),
            habit_id=habit_id,
            absence_date=absence_date,
            reason=reason,
        )

        try:
            self.session.add(absence)
            await self.session.commit()
            await self.session.refresh(absence)
            logger.info(
                "absence_created",
                habit_id=habit_id,
                date=str(absence_date),
                reason=reason,
            )
            return absence
        except IntegrityError:
            await self.session.rollback()
            # Race condition - absence was added by another request
            return await self.get_absence(habit_id, absence_date)

    async def get_absence(self, habit_id: str, absence_date: date) -> Absence | None:
        """Get a specific absence."""
        result = await self.session.execute(
            select(Absence).where(
                Absence.habit_id == habit_id,
                Absence.absence_date == absence_date,
            )
        )
        return result.scalar_one_or_none()

    async def delete_absence(self, habit_id: str, absence_date: date) -> bool:
        """Delete an absence."""
        absence = await self.get_absence(habit_id, absence_date)
        if not absence:
            return False

        await self.session.delete(absence)
        await self.session.commit()
        logger.info(
            "absence_deleted",
            habit_id=habit_id,
            date=str(absence_date),
        )
        return True

    async def get_absences(
        self,
        habit_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[tuple[date, str | None]]:
        """Get absences for a habit within a date range."""
        query = select(Absence.absence_date, Absence.reason).where(
            Absence.habit_id == habit_id
        )

        if start_date:
            query = query.where(Absence.absence_date >= start_date)
        if end_date:
            query = query.where(Absence.absence_date <= end_date)

        query = query.order_by(Absence.absence_date)
        result = await self.session.execute(query)
        return list(result.all())
