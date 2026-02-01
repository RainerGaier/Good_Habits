"""Health check tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    """Test the health check endpoint returns healthy status."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_api_root(client: AsyncClient) -> None:
    """Test the API root endpoint."""
    response = await client.get("/api/")
    assert response.status_code == 200
    assert "message" in response.json()
