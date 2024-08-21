import pytest
import asyncio
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_get_all_users():
    """
    Pytest for testing.

    :return: None.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
