from fastapi import APIRouter, Depends
from typing import List
from app.schemas.course import *
from app.services.course_service import CourseService
from app.services.dependencies import get_course_service
from app.schemas.course import CourseWithUsers

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseRead])
async def list_courses(
    service: CourseService = Depends(get_course_service),
    ):
    return await service.list_courses()

@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
    ):
    course = await service.get_course(course_id)
    if not course:
        return {"detail": "Course not found"}
    return course

@router.post("/", response_model=CourseCreateResponse)
async def create_course(
    course_in: CourseCreate,
    service: CourseService = Depends(get_course_service),
    ):
    course, created, response = await service.create_course(course_in)
    if not created:
        return response
    return course

@router.put("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int,
    course_in: CourseUpdate,
    service: CourseService = Depends(get_course_service),
    ):
    course, updated, response = await service.update_course(course_id, course_in)
    if not updated:
        return response
    return course

@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
    ):
    response = await service.delete_course(course_id)
    return response

@router.patch("/{course_id}/add_user/{user_id}", response_model=CourseWithUsers)
async def add_user_to_course(
    course_id: int,
    user_id: int,
    service: CourseService = Depends(get_course_service),
    ):
    return await service.add_user_to_course(course_id, user_id)

@router.get("/{course_id}/users", response_model=CourseWithUsers)
async def list_users_for_course(
    course_id: int,
    service: CourseService = Depends(get_course_service),
    ):
    return await service.get_course_with_users(course_id)

@router.delete("/{course_id}/remove_user/{user_id}", response_model=CourseWithUsers)
async def remove_user_from_course(
    course_id: int,
    user_id: int,
    service: CourseService = Depends(get_course_service),
    ):
    return await service.remove_user_from_course(course_id, user_id)
