"""Integration tests for Habit CRUD API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_habits_empty(client: AsyncClient) -> None:
    """Test listing habits when none exist."""
    response = await client.get("/api/habits")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_habit(client: AsyncClient) -> None:
    """Test creating a new habit."""
    response = await client.post(
        "/api/habits",
        json={"name": "Morning Meditation", "description": "10 minutes daily"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Morning Meditation"
    assert data["description"] == "10 minutes daily"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_habit_without_description(client: AsyncClient) -> None:
    """Test creating a habit without a description."""
    response = await client.post("/api/habits", json={"name": "Exercise"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Exercise"
    assert data["description"] is None


@pytest.mark.asyncio
async def test_create_habit_validation_error(client: AsyncClient) -> None:
    """Test validation error when name is empty."""
    response = await client.post("/api/habits", json={"name": ""})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_habit(client: AsyncClient) -> None:
    """Test getting a specific habit by ID."""
    # Create a habit first
    create_response = await client.post(
        "/api/habits", json={"name": "Reading", "description": "Read 30 pages"}
    )
    habit_id = create_response.json()["id"]

    # Get the habit
    response = await client.get(f"/api/habits/{habit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == habit_id
    assert data["name"] == "Reading"
    assert data["description"] == "Read 30 pages"


@pytest.mark.asyncio
async def test_get_habit_not_found(client: AsyncClient) -> None:
    """Test getting a non-existent habit."""
    response = await client.get("/api/habits/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_list_habits(client: AsyncClient) -> None:
    """Test listing multiple habits."""
    # Create habits
    await client.post("/api/habits", json={"name": "Habit 1"})
    await client.post("/api/habits", json={"name": "Habit 2"})

    response = await client.get("/api/habits")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [h["name"] for h in data]
    assert "Habit 1" in names
    assert "Habit 2" in names


@pytest.mark.asyncio
async def test_update_habit(client: AsyncClient) -> None:
    """Test updating a habit."""
    # Create a habit
    create_response = await client.post(
        "/api/habits", json={"name": "Old Name", "description": "Old description"}
    )
    habit_id = create_response.json()["id"]

    # Update the habit
    response = await client.put(
        f"/api/habits/{habit_id}",
        json={"name": "New Name", "description": "New description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "New description"


@pytest.mark.asyncio
async def test_update_habit_partial(client: AsyncClient) -> None:
    """Test partial update of a habit (only name)."""
    # Create a habit
    create_response = await client.post(
        "/api/habits", json={"name": "Original", "description": "Keep this"}
    )
    habit_id = create_response.json()["id"]

    # Update only name
    response = await client.put(f"/api/habits/{habit_id}", json={"name": "Updated"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["description"] == "Keep this"


@pytest.mark.asyncio
async def test_update_habit_not_found(client: AsyncClient) -> None:
    """Test updating a non-existent habit."""
    response = await client.put("/api/habits/nonexistent-id", json={"name": "New Name"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"


@pytest.mark.asyncio
async def test_delete_habit(client: AsyncClient) -> None:
    """Test deleting a habit."""
    # Create a habit
    create_response = await client.post("/api/habits", json={"name": "To Delete"})
    habit_id = create_response.json()["id"]

    # Delete the habit
    response = await client.delete(f"/api/habits/{habit_id}")
    assert response.status_code == 204

    # Verify it's gone
    get_response = await client.get(f"/api/habits/{habit_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_habit_not_found(client: AsyncClient) -> None:
    """Test deleting a non-existent habit."""
    response = await client.delete("/api/habits/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found"
