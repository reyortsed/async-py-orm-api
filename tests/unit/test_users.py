# tests/test_users.py

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(
    get_authenticated_client,  # Request the factory
    azure_ad_token: str       # Request the token
):
    # Use the factory to get a client configured with the Azure AD token
    authed_client: AsyncClient = get_authenticated_client(azure_ad_token)
    
    response = await authed_client.post("/users/", json={ # Use authed_client here
        "name": "Test User",
        "email": "test@example.com"
    })
    assert response.status_code == 200 # Or 201 for creation, depending on your API
    data = response.json()
    assert data["id"] > 0
    # Potentially assert other fields like name and email if they are returned
    # assert data["name"] == "Test User"
    # assert data["email"] == "test@example.com"

# ... other tests ...
    
@pytest.mark.asyncio
async def test_create_duplicate_user(get_authenticated_client, azure_ad_token):
    authed_client: AsyncClient = get_authenticated_client(azure_ad_token)
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    await authed_client.post("/users/", json=user_data)
    response = await authed_client.post("/users/", json=user_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "User email exists"

@pytest.mark.asyncio
async def test_get_user(get_authenticated_client, azure_ad_token):
    authed_client: AsyncClient = get_authenticated_client(azure_ad_token)
    create_resp = await authed_client.post("/users/", json={
        "name": "GetMe",
        "email": "getme@example.com"
    })
    user_id = create_resp.json()["id"]
    get_resp = await authed_client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == "getme@example.com"

@pytest.mark.asyncio
async def test_update_user(get_authenticated_client, azure_ad_token):
    authed_client: AsyncClient = get_authenticated_client(azure_ad_token)
    create_resp = await authed_client.post("/users/", json={
        "name": "UpdateMe",
        "email": "update@example.com"
    })
    user_id = create_resp.json()["id"]

    update_resp = await authed_client.put(f"/users/{user_id}", json={
        "name": "Updated Name"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_user(get_authenticated_client, azure_ad_token):
    authed_client: AsyncClient = get_authenticated_client(azure_ad_token)
    create_resp = await authed_client.post("/users/", json={
        "name": "DeleteMe",
        "email": "deleteme@example.com"
    })
    user_id = create_resp.json()["id"]

    delete_resp = await authed_client.delete(f"/users/{user_id}")
    assert delete_resp.status_code == 204

    followup = await authed_client.get(f"/users/{user_id}")
    assert followup.status_code == 404
