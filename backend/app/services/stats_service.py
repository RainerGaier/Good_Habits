"""Statistics service for streak and completion rate calculations."""

from datetime import date, timedelta

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.absence import Absence
from app.models.completion import Completion
from app.models.habit import Habit
from app.schemas.stats import CompletionRate, HabitWithStatsResponse

logger = structlog.get_logger()


class StatsService:
    """Service for calculating habit statistics."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize service with database session."""
        self.session = session

    async def _get_completion_dates(
        self,
        habit_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> set[date]:
        """Get set of completion dates for a habit."""
        query = select(Completion.completed_date).where(Completion.habit_id == habit_id)
        if start_date:
            query = query.where(Completion.completed_date >= start_date)
        if end_date:
            query = query.where(Completion.completed_date <= end_date)
        result = await self.session.execute(query)
        return set(result.scalars().all())

    async def _get_absence_dates(
        self,
        habit_id: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> set[date]:
        """Get set of absence dates for a habit."""
        query = select(Absence.absence_date).where(Absence.habit_id == habit_id)
        if start_date:
            query = query.where(Absence.absence_date >= start_date)
        if end_date:
            query = query.where(Absence.absence_date <= end_date)
        result = await self.session.execute(query)
        return set(result.scalars().all())

    async def _get_habit_created_date(self, habit_id: str) -> date | None:
        """Get the creation date of a habit."""
        result = await self.session.execute(
            select(Habit.created_at).where(Habit.id == habit_id)
        )
        created_at = result.scalar_one_or_none()
        if created_at:
            return created_at.date()
        return None

    async def calculate_current_streak(self, habit_id: str) -> int:
        """Calculate current consecutive streak for a habit.

        Rules:
        - Streak counts consecutive days where completion exists
        - Absences preserve streak but don't add to count
        - Streak breaks when no completion AND no absence
        - If today not completed, start counting from yesterday
        """
        today = date.today()
        completions = await self._get_completion_dates(habit_id)
        absences = await self._get_absence_dates(habit_id)

        if not completions:
            return 0

        # Determine starting point
        current_day = today if today in completions else today - timedelta(days=1)

        streak = 0
        while True:
            if current_day in completions:
                streak += 1
                current_day -= timedelta(days=1)
            elif current_day in absences:
                # Absence preserves streak but doesn't add to count
                current_day -= timedelta(days=1)
            else:
                # Neither completion nor absence - streak breaks
                break

        return streak

    async def calculate_best_streak(self, habit_id: str) -> int:
        """Calculate the longest streak ever achieved for a habit.

        Scans all days from first completion to today and tracks max streak.
        """
        completions = await self._get_completion_dates(habit_id)
        absences = await self._get_absence_dates(habit_id)

        if not completions:
            return 0

        # Find the earliest completion date
        first_completion = min(completions)
        today = date.today()

        best_streak = 0
        current_streak = 0
        current_day = first_completion

        while current_day <= today:
            if current_day in completions:
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            elif current_day in absences:
                # Absence preserves streak but doesn't add
                pass
            else:
                # Gap breaks the streak
                current_streak = 0

            current_day += timedelta(days=1)

        return best_streak

    async def calculate_completion_rate(self, habit_id: str) -> CompletionRate:
        """Calculate completion rates excluding absence days.

        Returns rates for:
        - week: Last 7 days
        - month: Last 30 days
        - all_time: Since habit creation
        """
        today = date.today()

        # Weekly rate (last 7 days)
        week_start = today - timedelta(days=6)
        week_rate = await self._calculate_rate_for_period(habit_id, week_start, today)

        # Monthly rate (last 30 days)
        month_start = today - timedelta(days=29)
        month_rate = await self._calculate_rate_for_period(habit_id, month_start, today)

        # All-time rate
        created_date = await self._get_habit_created_date(habit_id)
        if created_date:
            all_time_rate = await self._calculate_rate_for_period(
                habit_id, created_date, today
            )
        else:
            all_time_rate = 0.0

        return CompletionRate(
            week=round(week_rate, 1),
            month=round(month_rate, 1),
            all_time=round(all_time_rate, 1),
        )

    async def _calculate_rate_for_period(
        self, habit_id: str, start_date: date, end_date: date
    ) -> float:
        """Calculate completion rate for a specific period.

        Rate = completions / (total_days - absence_days)
        """
        completions = await self._get_completion_dates(habit_id, start_date, end_date)
        absences = await self._get_absence_dates(habit_id, start_date, end_date)

        total_days = (end_date - start_date).days + 1
        absence_days = len(absences)
        applicable_days = total_days - absence_days

        if applicable_days <= 0:
            return 0.0

        completion_count = len(completions)
        return (completion_count / applicable_days) * 100

    async def is_completed_today(self, habit_id: str) -> bool:
        """Check if habit is completed for today."""
        today = date.today()
        result = await self.session.execute(
            select(func.count())
            .select_from(Completion)
            .where(Completion.habit_id == habit_id, Completion.completed_date == today)
        )
        count = result.scalar_one()
        return count > 0

    async def get_habit_with_stats(
        self, habit_id: str
    ) -> HabitWithStatsResponse | None:
        """Get a habit with all computed statistics."""
        result = await self.session.execute(select(Habit).where(Habit.id == habit_id))
        habit = result.scalar_one_or_none()

        if not habit:
            return None

        current_streak = await self.calculate_current_streak(habit_id)
        best_streak = await self.calculate_best_streak(habit_id)
        completion_rate = await self.calculate_completion_rate(habit_id)
        completed_today = await self.is_completed_today(habit_id)

        return HabitWithStatsResponse(
            id=habit.id,
            name=habit.name,
            description=habit.description,
            created_at=habit.created_at,
            updated_at=habit.updated_at,
            current_streak=current_streak,
            best_streak=best_streak,
            completion_rate=completion_rate,
            completed_today=completed_today,
        )

    async def get_all_habits_with_stats(self) -> list[HabitWithStatsResponse]:
        """Get all habits with computed statistics."""
        result = await self.session.execute(select(Habit))
        habits = result.scalars().all()

        habits_with_stats = []
        for habit in habits:
            stats = await self.get_habit_with_stats(habit.id)
            if stats:
                habits_with_stats.append(stats)

        return habits_with_stats
