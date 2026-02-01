"""Integration tests for Completion tracking API endpoints."""

from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.fixture
async def habit_id(client: AsyncClient) -> str:
    """Create a habit and return its ID for testing completions."""
    response = await client.post(
        "/api/habits", json={"name": "Test Habit", "description": "For testing"}
    )
    return response.json()["id"]


@pytest.mark.asyncio
async def test_complete_habit_today(client: AsyncClient, habit_id: str) -> None:
    """Test completing a habit for today (default)."""
    response = await client.post(f"/api/habits/{habit_id}/complete", json={})
    assert response.status_code == 201
    data = response.json()
    assert data["habit_id"] == habit_id
    assert data["date"] == str(date.today())
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_complete_habit_specific_date(client: AsyncClient, habit_id: str) -> None:
    """Test completing a habit for a specific date."""
    specific_date = date(2024, 1, 15)
    response = await client.post(
        f"/api/habits/{habit_id}/complete", json={"date": str(specific_date)}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["date"] == str(specific_date)


@pytest.mark.asyncio
async def test_complete_habit_idempotent(client: AsyncClient, habit_id: str) -> None:
    """Test that completing the same date twice returns existing completion."""
    specific_date = str(date.today())

    # First completion
    response1 = await client.post(
        f"/api/habits/{habit_id}/complete", json={"date": specific_date}
    )
    assert response1.status_code == 201

    # Second completion (same date)
    response2 = await client.post(
        f"/api/habits/{habit_id}/complete", json={"date": specific_date}
    )
    assert response2.status_code == 201
    assert response2.json()["date"] == specific_date


@pytest.mark.asyncio
async def test_complete_habit_not_found(client: AsyncClient) -> None:
    """Test completing a non-existent habit."""
    response = await client.post("/api/habits/nonexistent-id/complete", json={})
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_get_completions_empty(client: AsyncClient, habit_id: str) -> None:
    """Test getting completions when none exist."""
    response = await client.get(f"/api/habits/{habit_id}/completions")
    assert response.status_code == 200
    data = response.json()
    assert data["habit_id"] == habit_id
    assert data["completions"] == []


@pytest.mark.asyncio
async def test_get_completions(client: AsyncClient, habit_id: str) -> None:
    """Test getting completion history."""
    # Create some completions
    dates = [date.today() - timedelta(days=i) for i in range(3)]
    for d in dates:
        await client.post(f"/api/habits/{habit_id}/complete", json={"date": str(d)})

    response = await client.get(f"/api/habits/{habit_id}/completions")
    assert response.status_code == 200
    data = response.json()
    assert data["habit_id"] == habit_id
    assert len(data["completions"]) == 3


@pytest.mark.asyncio
async def test_get_completions_date_range(client: AsyncClient, habit_id: str) -> None:
    """Test getting completions within a date range."""
    # Create completions for the past 10 days
    base_date = date.today()
    for i in range(10):
        d = base_date - timedelta(days=i)
        await client.post(f"/api/habits/{habit_id}/complete", json={"date": str(d)})

    # Query for last 5 days only
    start = base_date - timedelta(days=4)
    end = base_date

    response = await client.get(
        f"/api/habits/{habit_id}/completions",
        params={"start_date": str(start), "end_date": str(end)},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["completions"]) == 5


@pytest.mark.asyncio
async def test_get_completions_habit_not_found(client: AsyncClient) -> None:
    """Test getting completions for a non-existent habit."""
    response = await client.get("/api/habits/nonexistent-id/completions")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_delete_completion(client: AsyncClient, habit_id: str) -> None:
    """Test deleting a completion (undo)."""
    completion_date = str(date.today())

    # Create a completion
    await client.post(
        f"/api/habits/{habit_id}/complete", json={"date": completion_date}
    )

    # Delete the completion
    response = await client.delete(
        f"/api/habits/{habit_id}/completions/{completion_date}"
    )
    assert response.status_code == 204

    # Verify it's gone
    get_response = await client.get(f"/api/habits/{habit_id}/completions")
    assert len(get_response.json()["completions"]) == 0


@pytest.mark.asyncio
async def test_delete_completion_not_found(client: AsyncClient, habit_id: str) -> None:
    """Test deleting a non-existent completion."""
    response = await client.delete(f"/api/habits/{habit_id}/completions/2024-01-01")
    assert response.status_code == 404
    assert response.json()["detail"] == "Completion not found"


@pytest.mark.asyncio
async def test_delete_completion_habit_not_found(client: AsyncClient) -> None:
    """Test deleting completion for a non-existent habit."""
    response = await client.delete("/api/habits/nonexistent-id/completions/2024-01-01")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_cascade_delete_completions(client: AsyncClient, habit_id: str) -> None:
    """Test that completions are deleted when habit is deleted."""
    # Create some completions
    await client.post(f"/api/habits/{habit_id}/complete", json={"date": "2024-01-01"})
    await client.post(f"/api/habits/{habit_id}/complete", json={"date": "2024-01-02"})

    # Verify completions exist
    get_response = await client.get(f"/api/habits/{habit_id}/completions")
    assert len(get_response.json()["completions"]) == 2

    # Delete the habit
    await client.delete(f"/api/habits/{habit_id}")

    # Verify habit is gone
    response = await client.get(f"/api/habits/{habit_id}")
    assert response.status_code == 404
