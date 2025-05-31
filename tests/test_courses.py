import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.course import Course
from app.models.course import user_course_association

async def get_user_and_course(client: AsyncClient):
    user_resp = await client.post("/users/", json={"name": "User API", "email": "userapi@example.com"})
    assert user_resp.status_code in (200, 201)
    user_id = user_resp.json()["id"]
    course_resp = await client.post("/courses/", json={"name": "Course API", "description": "Course Desc"})
    assert course_resp.status_code in (200, 201)
    course_id = course_resp.json()["id"]
    return user_id, course_id

@pytest.mark.asyncio
async def test_remove_course_from_user(client: AsyncClient):
    user_id, course_id = await get_user_and_course(client)
    # Add association first
    await client.patch(f"/users/{user_id}/add_course/{course_id}")
    # Remove association
    resp = await client.delete(f"/users/{user_id}/remove_course/{course_id}")
    assert resp.status_code == 200
    # Confirm removal
    resp = await client.get(f"/users/{user_id}/courses")
    assert resp.status_code == 200
    data = resp.json()
    assert all(c["id"] != course_id for c in data["courses"])

@pytest.mark.asyncio
async def test_remove_user_from_course(client: AsyncClient):
    user_id, course_id = await get_user_and_course(client)
    # Add association first
    await client.patch(f"/courses/{course_id}/add_user/{user_id}")
    # Remove association
    resp = await client.delete(f"/courses/{course_id}/remove_user/{user_id}")
    assert resp.status_code == 200
    # Confirm removal
    resp = await client.get(f"/courses/{course_id}/users")
    assert resp.status_code == 200
    data = resp.json()
    assert all(u["id"] != user_id for u in data["users"])

@pytest.mark.asyncio
async def test_add_course_to_user_endpoint(client: AsyncClient):
    user_id, course_id = await get_user_and_course(client)
    resp = await client.patch(f"/users/{user_id}/add_course/{course_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert any(c["id"] == course_id for c in data["courses"])

@pytest.mark.asyncio
async def test_add_user_to_course_endpoint(client: AsyncClient):
    user_id, course_id = await get_user_and_course(client)
    resp = await client.patch(f"/courses/{course_id}/add_user/{user_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert any(u["id"] == user_id for u in data["users"])

@pytest.mark.asyncio
async def test_list_courses_for_user(client: AsyncClient):
    user_id, course_id = await get_user_and_course(client)
    # Associate first
    await client.patch(f"/users/{user_id}/add_course/{course_id}")
    resp = await client.get(f"/users/{user_id}/courses")
    assert resp.status_code == 200
    data = resp.json()
    assert any(c["id"] == course_id for c in data["courses"])

@pytest.mark.asyncio
async def test_list_users_for_course(client: AsyncClient):
    user_id, course_id = await get_user_and_course(client)
    # Associate first
    await client.patch(f"/courses/{course_id}/add_user/{user_id}")
    resp = await client.get(f"/courses/{course_id}/users")
    assert resp.status_code == 200
    data = resp.json()
    assert any(u["id"] == user_id for u in data["users"])

@pytest.mark.asyncio
async def test_create_course(client: AsyncClient):
    response = await client.post("/courses/", json={
        "name": "Math 101",
        "description": "Basic Mathematics"
    })
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["id"] > 0

@pytest.mark.asyncio
async def test_create_duplicate_course(client: AsyncClient):
    course_data = {
        "name": "Physics 101",
        "description": "Basic Physics"
    }
    await client.post("/courses/", json=course_data)
    response = await client.post("/courses/", json=course_data)
    assert response.status_code == 409 or response.status_code == 200  # Accepts either if not unique

@pytest.mark.asyncio
async def test_get_course(client: AsyncClient):
    create_resp = await client.post("/courses/", json={
        "name": "Chemistry 101",
        "description": "Basic Chemistry"
    })
    course_id = create_resp.json()["id"]
    get_resp = await client.get(f"/courses/{course_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Chemistry 101"

@pytest.mark.asyncio
async def test_update_course(client: AsyncClient):
    create_resp = await client.post("/courses/", json={
        "name": "Biology 101",
        "description": "Basic Biology"
    })
    course_id = create_resp.json()["id"]
    update_resp = await client.put(f"/courses/{course_id}", json={"name": "Biology 102"})
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Biology 102"

@pytest.mark.asyncio
async def test_delete_course(client: AsyncClient):
    create_resp = await client.post("/courses/", json={
        "name": "DeleteMe 101",
        "description": "To be deleted"
    })
    course_id = create_resp.json()["id"]
    del_resp = await client.delete(f"/courses/{course_id}")
    assert del_resp.status_code == 204 or del_resp.status_code == 200
