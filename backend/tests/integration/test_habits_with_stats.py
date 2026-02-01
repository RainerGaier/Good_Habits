"""Integration tests for enhanced habits endpoint with statistics."""

from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_habits_with_stats_empty(client: AsyncClient) -> None:
    """Test listing habits when none exist."""
    response = await client.get("/api/habits")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_habits_includes_stats(client: AsyncClient) -> None:
    """Test that habit list includes all stat fields."""
    # Create a habit
    create_response = await client.post(
        "/api/habits", json={"name": "Test Habit", "description": "Testing stats"}
    )
    assert create_response.status_code == 201

    # Get habits list
    response = await client.get("/api/habits")
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) == 1

    habit = habits[0]
    assert "id" in habit
    assert "name" in habit
    assert habit["name"] == "Test Habit"
    assert "current_streak" in habit
    assert "best_streak" in habit
    assert "completion_rate" in habit
    assert "completed_today" in habit

    # Check completion_rate structure
    assert "week" in habit["completion_rate"]
    assert "month" in habit["completion_rate"]
    assert "all_time" in habit["completion_rate"]


@pytest.mark.asyncio
async def test_list_habits_current_streak(client: AsyncClient) -> None:
    """Test that current streak is calculated correctly."""
    # Create a habit
    create_response = await client.post("/api/habits", json={"name": "Streak Habit"})
    habit_id = create_response.json()["id"]

    # Complete habit for last 3 days including today
    today = date.today()
    for i in range(3):
        await client.post(
            f"/api/habits/{habit_id}/complete",
            json={"date": str(today - timedelta(days=i))},
        )

    # Get habits list
    response = await client.get("/api/habits")
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) == 1
    assert habits[0]["current_streak"] == 3


@pytest.mark.asyncio
async def test_list_habits_completed_today(client: AsyncClient) -> None:
    """Test completed_today flag is correct."""
    # Create a habit
    create_response = await client.post("/api/habits", json={"name": "Today Habit"})
    habit_id = create_response.json()["id"]

    # Initially not completed
    response1 = await client.get("/api/habits")
    assert response1.json()[0]["completed_today"] is False

    # Complete today
    await client.post(f"/api/habits/{habit_id}/complete", json={})

    # Now should be completed
    response2 = await client.get("/api/habits")
    assert response2.json()[0]["completed_today"] is True


@pytest.mark.asyncio
async def test_list_habits_completion_rate(client: AsyncClient) -> None:
    """Test completion rate calculations."""
    # Create a habit
    create_response = await client.post("/api/habits", json={"name": "Rate Habit"})
    habit_id = create_response.json()["id"]

    # Complete habit for 5 of the last 7 days
    today = date.today()
    for i in range(5):
        await client.post(
            f"/api/habits/{habit_id}/complete",
            json={"date": str(today - timedelta(days=i))},
        )

    # Get habits list
    response = await client.get("/api/habits")
    assert response.status_code == 200
    habits = response.json()

    # Weekly rate should be approximately 71.4% (5/7)
    assert 70 <= habits[0]["completion_rate"]["week"] <= 73


@pytest.mark.asyncio
async def test_list_habits_streak_with_absence(client: AsyncClient) -> None:
    """Test that absences preserve streak."""
    # Create a habit
    create_response = await client.post("/api/habits", json={"name": "Absence Habit"})
    habit_id = create_response.json()["id"]

    today = date.today()

    # Complete today
    await client.post(f"/api/habits/{habit_id}/complete", json={"date": str(today)})
    # Mark yesterday as absence
    await client.post(
        f"/api/habits/{habit_id}/absences",
        json={"date": str(today - timedelta(days=1))},
    )
    # Complete day before yesterday
    await client.post(
        f"/api/habits/{habit_id}/complete",
        json={"date": str(today - timedelta(days=2))},
    )

    # Get habits list
    response = await client.get("/api/habits")
    assert response.status_code == 200
    habits = response.json()

    # Streak should be 2 (today + day-before-yesterday, absence preserved but didn't add)
    assert habits[0]["current_streak"] == 2


@pytest.mark.asyncio
async def test_list_multiple_habits_with_stats(client: AsyncClient) -> None:
    """Test listing multiple habits each with their own stats."""
    # Create two habits
    response1 = await client.post("/api/habits", json={"name": "Habit 1"})
    habit1_id = response1.json()["id"]

    response2 = await client.post("/api/habits", json={"name": "Habit 2"})
    habit2_id = response2.json()["id"]

    today = date.today()

    # Complete habit 1 for 3 days
    for i in range(3):
        await client.post(
            f"/api/habits/{habit1_id}/complete",
            json={"date": str(today - timedelta(days=i))},
        )

    # Complete habit 2 for 1 day
    await client.post(f"/api/habits/{habit2_id}/complete", json={"date": str(today)})

    # Get habits list
    response = await client.get("/api/habits")
    assert response.status_code == 200
    habits = response.json()
    assert len(habits) == 2

    # Find each habit by name and check streak
    habit1 = next(h for h in habits if h["name"] == "Habit 1")
    habit2 = next(h for h in habits if h["name"] == "Habit 2")

    assert habit1["current_streak"] == 3
    assert habit2["current_streak"] == 1
