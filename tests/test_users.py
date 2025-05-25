# tests/test_users.py

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/users/", json={
        "name": "Test User",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    
@pytest.mark.asyncio
async def test_create_duplicate_user(client: AsyncClient):
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    await client.post("/users/", json=user_data)
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "User email exists"

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    create_resp = await client.post("/users/", json={
        "name": "GetMe",
        "email": "getme@example.com"
    })
    user_id = create_resp.json()["id"]
    get_resp = await client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "getme@example.com"

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    create_resp = await client.post("/users/", json={
        "name": "UpdateMe",
        "email": "update@example.com"
    })
    user_id = create_resp.json()["id"]

    update_resp = await client.put(f"/users/{user_id}", json={
        "name": "Updated Name"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    create_resp = await client.post("/users/", json={
        "name": "DeleteMe",
        "email": "deleteme@example.com"
    })
    user_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/users/{user_id}")
    assert delete_resp.status_code == 204

    followup = await client.get(f"/users/{user_id}")
    assert followup.status_code == 404
