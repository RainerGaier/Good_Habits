"""Integration tests for Absence tracking API endpoints."""

from datetime import date, timedelta

import pytest
from httpx import AsyncClient


@pytest.fixture
async def habit_id(client: AsyncClient) -> str:
    """Create a habit and return its ID for testing absences."""
    response = await client.post(
        "/api/habits", json={"name": "Test Habit", "description": "For testing"}
    )
    return response.json()["id"]


@pytest.mark.asyncio
async def test_create_absence_today(client: AsyncClient, habit_id: str) -> None:
    """Test creating an absence for today (default)."""
    response = await client.post(f"/api/habits/{habit_id}/absences", json={})
    assert response.status_code == 201
    data = response.json()
    assert data["habit_id"] == habit_id
    assert data["date"] == str(date.today())
    assert data["reason"] is None


@pytest.mark.asyncio
async def test_create_absence_specific_date(client: AsyncClient, habit_id: str) -> None:
    """Test creating an absence for a specific date."""
    specific_date = date(2024, 1, 15)
    response = await client.post(
        f"/api/habits/{habit_id}/absences", json={"date": str(specific_date)}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["date"] == str(specific_date)


@pytest.mark.asyncio
async def test_create_absence_with_reason(client: AsyncClient, habit_id: str) -> None:
    """Test creating an absence with a reason."""
    response = await client.post(
        f"/api/habits/{habit_id}/absences",
        json={"date": "2024-02-01", "reason": "vacation"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["reason"] == "vacation"


@pytest.mark.asyncio
async def test_create_absence_idempotent(client: AsyncClient, habit_id: str) -> None:
    """Test that creating the same absence twice returns existing."""
    specific_date = str(date.today())

    # First absence
    response1 = await client.post(
        f"/api/habits/{habit_id}/absences", json={"date": specific_date}
    )
    assert response1.status_code == 201

    # Second absence (same date)
    response2 = await client.post(
        f"/api/habits/{habit_id}/absences", json={"date": specific_date}
    )
    assert response2.status_code == 201
    assert response2.json()["date"] == specific_date


@pytest.mark.asyncio
async def test_create_absence_habit_not_found(client: AsyncClient) -> None:
    """Test creating an absence for a non-existent habit."""
    response = await client.post("/api/habits/nonexistent-id/absences", json={})
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_get_absences_empty(client: AsyncClient, habit_id: str) -> None:
    """Test getting absences when none exist."""
    response = await client.get(f"/api/habits/{habit_id}/absences")
    assert response.status_code == 200
    data = response.json()
    assert data["habit_id"] == habit_id
    assert data["absences"] == []


@pytest.mark.asyncio
async def test_get_absences_with_data(client: AsyncClient, habit_id: str) -> None:
    """Test getting absence history."""
    # Create some absences
    dates = [date.today() - timedelta(days=i) for i in range(3)]
    for d in dates:
        await client.post(
            f"/api/habits/{habit_id}/absences",
            json={"date": str(d), "reason": "sick"},
        )

    response = await client.get(f"/api/habits/{habit_id}/absences")
    assert response.status_code == 200
    data = response.json()
    assert data["habit_id"] == habit_id
    assert len(data["absences"]) == 3


@pytest.mark.asyncio
async def test_get_absences_date_range(client: AsyncClient, habit_id: str) -> None:
    """Test getting absences within a date range."""
    # Create absences for the past 10 days
    base_date = date.today()
    for i in range(10):
        d = base_date - timedelta(days=i)
        await client.post(f"/api/habits/{habit_id}/absences", json={"date": str(d)})

    # Query for last 5 days only
    start = base_date - timedelta(days=4)
    end = base_date

    response = await client.get(
        f"/api/habits/{habit_id}/absences",
        params={"start_date": str(start), "end_date": str(end)},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["absences"]) == 5


@pytest.mark.asyncio
async def test_get_absences_habit_not_found(client: AsyncClient) -> None:
    """Test getting absences for a non-existent habit."""
    response = await client.get("/api/habits/nonexistent-id/absences")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_delete_absence(client: AsyncClient, habit_id: str) -> None:
    """Test deleting an absence."""
    absence_date = str(date.today())

    # Create an absence
    await client.post(f"/api/habits/{habit_id}/absences", json={"date": absence_date})

    # Delete the absence
    response = await client.delete(f"/api/habits/{habit_id}/absences/{absence_date}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = await client.get(f"/api/habits/{habit_id}/absences")
    assert len(get_response.json()["absences"]) == 0


@pytest.mark.asyncio
async def test_delete_absence_not_found(client: AsyncClient, habit_id: str) -> None:
    """Test deleting a non-existent absence."""
    response = await client.delete(f"/api/habits/{habit_id}/absences/2024-01-01")
    assert response.status_code == 404
    assert response.json()["detail"] == "Absence not found"


@pytest.mark.asyncio
async def test_delete_absence_habit_not_found(client: AsyncClient) -> None:
    """Test deleting absence for a non-existent habit."""
    response = await client.delete("/api/habits/nonexistent-id/absences/2024-01-01")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_cascade_delete_absences(client: AsyncClient, habit_id: str) -> None:
    """Test that absences are deleted when habit is deleted."""
    # Create some absences
    await client.post(f"/api/habits/{habit_id}/absences", json={"date": "2024-01-01"})
    await client.post(f"/api/habits/{habit_id}/absences", json={"date": "2024-01-02"})

    # Verify absences exist
    get_response = await client.get(f"/api/habits/{habit_id}/absences")
    assert len(get_response.json()["absences"]) == 2

    # Delete the habit
    await client.delete(f"/api/habits/{habit_id}")

    # Verify habit is gone
    response = await client.get(f"/api/habits/{habit_id}")
    assert response.status_code == 404
