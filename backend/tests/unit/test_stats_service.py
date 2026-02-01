"""Unit tests for StatsService streak and rate calculations."""

import uuid
from datetime import date, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.absence import Absence
from app.models.completion import Completion
from app.models.habit import Habit
from app.services.stats_service import StatsService


async def create_habit(session: AsyncSession, name: str = "Test Habit") -> Habit:
    """Helper to create a test habit."""
    habit = Habit(name=name)
    session.add(habit)
    await session.commit()
    await session.refresh(habit)
    return habit


async def create_completion(
    session: AsyncSession, habit_id: str, completion_date: date
) -> Completion:
    """Helper to create a test completion."""
    completion = Completion(
        id=str(uuid.uuid4()),
        habit_id=habit_id,
        completed_date=completion_date,
    )
    session.add(completion)
    await session.commit()
    return completion


async def create_absence(
    session: AsyncSession, habit_id: str, absence_date: date, reason: str | None = None
) -> Absence:
    """Helper to create a test absence."""
    absence = Absence(
        id=str(uuid.uuid4()),
        habit_id=habit_id,
        absence_date=absence_date,
        reason=reason,
    )
    session.add(absence)
    await session.commit()
    return absence


@pytest.mark.asyncio
async def test_current_streak_no_completions(db_session: AsyncSession) -> None:
    """Test current streak returns 0 when no completions exist."""
    habit = await create_habit(db_session)
    service = StatsService(db_session)

    streak = await service.calculate_current_streak(habit.id)
    assert streak == 0


@pytest.mark.asyncio
async def test_current_streak_consecutive_days(db_session: AsyncSession) -> None:
    """Test current streak counts consecutive completed days."""
    habit = await create_habit(db_session)
    today = date.today()

    # Complete the last 5 days including today
    for i in range(5):
        await create_completion(db_session, habit.id, today - timedelta(days=i))

    service = StatsService(db_session)
    streak = await service.calculate_current_streak(habit.id)
    assert streak == 5


@pytest.mark.asyncio
async def test_current_streak_with_gap(db_session: AsyncSession) -> None:
    """Test streak breaks at a gap."""
    habit = await create_habit(db_session)
    today = date.today()

    # Complete today and yesterday
    await create_completion(db_session, habit.id, today)
    await create_completion(db_session, habit.id, today - timedelta(days=1))
    # Skip day 2
    # Complete days 3, 4, 5
    await create_completion(db_session, habit.id, today - timedelta(days=3))
    await create_completion(db_session, habit.id, today - timedelta(days=4))
    await create_completion(db_session, habit.id, today - timedelta(days=5))

    service = StatsService(db_session)
    streak = await service.calculate_current_streak(habit.id)
    assert streak == 2  # Only today and yesterday count


@pytest.mark.asyncio
async def test_current_streak_with_absence(db_session: AsyncSession) -> None:
    """Test absence preserves streak but doesn't add to count."""
    habit = await create_habit(db_session)
    today = date.today()

    # Complete today
    await create_completion(db_session, habit.id, today)
    # Mark yesterday as absence
    await create_absence(db_session, habit.id, today - timedelta(days=1))
    # Complete day before that
    await create_completion(db_session, habit.id, today - timedelta(days=2))
    await create_completion(db_session, habit.id, today - timedelta(days=3))

    service = StatsService(db_session)
    streak = await service.calculate_current_streak(habit.id)
    # Streak should be 3: today + day-2 + day-3 (absence doesn't add but doesn't break)
    assert streak == 3


@pytest.mark.asyncio
async def test_current_streak_today_not_completed(db_session: AsyncSession) -> None:
    """Test streak counts from yesterday if today not completed."""
    habit = await create_habit(db_session)
    today = date.today()

    # Complete yesterday and day before, but not today
    await create_completion(db_session, habit.id, today - timedelta(days=1))
    await create_completion(db_session, habit.id, today - timedelta(days=2))
    await create_completion(db_session, habit.id, today - timedelta(days=3))

    service = StatsService(db_session)
    streak = await service.calculate_current_streak(habit.id)
    assert streak == 3


@pytest.mark.asyncio
async def test_best_streak_calculation(db_session: AsyncSession) -> None:
    """Test best streak finds the longest historical streak."""
    habit = await create_habit(db_session)
    today = date.today()

    # Create a 3-day streak ending today
    await create_completion(db_session, habit.id, today)
    await create_completion(db_session, habit.id, today - timedelta(days=1))
    await create_completion(db_session, habit.id, today - timedelta(days=2))
    # Gap
    # Create a 5-day streak in the past
    await create_completion(db_session, habit.id, today - timedelta(days=10))
    await create_completion(db_session, habit.id, today - timedelta(days=11))
    await create_completion(db_session, habit.id, today - timedelta(days=12))
    await create_completion(db_session, habit.id, today - timedelta(days=13))
    await create_completion(db_session, habit.id, today - timedelta(days=14))

    service = StatsService(db_session)
    best = await service.calculate_best_streak(habit.id)
    assert best == 5  # The older 5-day streak is the best


@pytest.mark.asyncio
async def test_completion_rate_weekly(db_session: AsyncSession) -> None:
    """Test weekly completion rate calculation."""
    habit = await create_habit(db_session)
    today = date.today()

    # Complete 5 of the last 7 days
    for i in range(5):
        await create_completion(db_session, habit.id, today - timedelta(days=i))

    service = StatsService(db_session)
    rate = await service.calculate_completion_rate(habit.id)

    # 5/7 = 71.4%
    assert rate.week == pytest.approx(71.4, abs=0.1)


@pytest.mark.asyncio
async def test_completion_rate_excludes_absences(db_session: AsyncSession) -> None:
    """Test completion rate excludes absence days from denominator."""
    habit = await create_habit(db_session)
    today = date.today()

    # Complete 3 days
    await create_completion(db_session, habit.id, today)
    await create_completion(db_session, habit.id, today - timedelta(days=1))
    await create_completion(db_session, habit.id, today - timedelta(days=2))
    # Mark 2 days as absences
    await create_absence(db_session, habit.id, today - timedelta(days=3))
    await create_absence(db_session, habit.id, today - timedelta(days=4))
    # Leave days 5 and 6 as missed

    service = StatsService(db_session)
    rate = await service.calculate_completion_rate(habit.id)

    # 7 days - 2 absences = 5 applicable days
    # 3 completions / 5 applicable = 60%
    assert rate.week == pytest.approx(60.0, abs=0.1)


@pytest.mark.asyncio
async def test_completed_today_true(db_session: AsyncSession) -> None:
    """Test is_completed_today returns true when completed."""
    habit = await create_habit(db_session)
    await create_completion(db_session, habit.id, date.today())

    service = StatsService(db_session)
    assert await service.is_completed_today(habit.id) is True


@pytest.mark.asyncio
async def test_completed_today_false(db_session: AsyncSession) -> None:
    """Test is_completed_today returns false when not completed."""
    habit = await create_habit(db_session)
    # Complete yesterday, not today
    await create_completion(db_session, habit.id, date.today() - timedelta(days=1))

    service = StatsService(db_session)
    assert await service.is_completed_today(habit.id) is False


@pytest.mark.asyncio
async def test_get_habit_with_stats(db_session: AsyncSession) -> None:
    """Test get_habit_with_stats returns all statistics."""
    habit = await create_habit(db_session, "Stats Test Habit")
    today = date.today()

    # Create some completions
    await create_completion(db_session, habit.id, today)
    await create_completion(db_session, habit.id, today - timedelta(days=1))

    service = StatsService(db_session)
    stats = await service.get_habit_with_stats(habit.id)

    assert stats is not None
    assert stats.id == habit.id
    assert stats.name == "Stats Test Habit"
    assert stats.current_streak == 2
    assert stats.best_streak == 2
    assert stats.completed_today is True
    assert stats.completion_rate.week >= 0


@pytest.mark.asyncio
async def test_get_habit_with_stats_not_found(db_session: AsyncSession) -> None:
    """Test get_habit_with_stats returns None for non-existent habit."""
    service = StatsService(db_session)
    stats = await service.get_habit_with_stats("nonexistent-id")
    assert stats is None
