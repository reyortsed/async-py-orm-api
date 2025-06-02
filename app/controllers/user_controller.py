
from fastapi import APIRouter, Depends
from typing import List
from app.schemas.user import *
from app.services.user_service import UserService
from app.services.dependencies import get_user_service
from app.resources import responses
from app.schemas.user import UserWithCourses
from typing import List
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


async def list_users(service: UserService = Depends(get_user_service)):
    return await service.list_users()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    ):
    user = await service.get_user(user_id)
    if not user:
        return responses.user_not_found
    return user

@router.post("/", response_model=UserCreateResponse)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
    ):
    user, created, response = await service.create_user_if_not_exists(user_in)
    if not created:
        return response
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service),
    ):
    user, updated, response = await service.update_user(user_id, user_in)
    if not updated:
        return response
    return user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    ):
    response = await service.delete_user(user_id)
    return response

@router.patch("/{user_id}/add_course/{course_id}", response_model=UserWithCourses)
async def add_course_to_user(
    user_id: int,
    course_id: int,
    service: UserService = Depends(get_user_service),
    ):
    return await service.add_course_to_user(user_id, course_id)

@router.get("/{user_id}/courses", response_model=UserWithCourses)
async def list_courses_for_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    ):
    return await service.get_user_with_courses(user_id)

@router.delete("/{user_id}/remove_course/{course_id}", response_model=UserWithCourses)
async def remove_course_from_user(
    user_id: int,
    course_id: int,
    service: UserService = Depends(get_user_service),
    ):
    return await service.remove_course_from_user(user_id, course_id)
