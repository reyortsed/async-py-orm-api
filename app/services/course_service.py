from http import HTTPStatus
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.course_repository import CourseRepository
from app.schemas.course import CourseCreate, CourseUpdate
from typing import Sequence, Optional
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseWithUsers

class CourseService:
    def __init__(self, db: AsyncSession):
        self.repo = CourseRepository(db)
        self.db = db

    async def list_courses(self) -> Sequence[Course]:
        return await self.repo.get_all()

    async def get_course(self, course_id: int) -> Optional[Course]:
        return await self.repo.get_by_id(course_id)

    async def create_course(self, course_in: CourseCreate) -> tuple[Course, bool, JSONResponse]:
        try:
            course = await self.repo.create(course_in)
            await self.db.commit()
            await self.db.refresh(course)
            return course, True, JSONResponse(status_code=HTTPStatus.CREATED, content={"detail": "Course created"})
        except IntegrityError as ex:
            await self.db.rollback()
            return None, False, JSONResponse(status_code=HTTPStatus.CONFLICT, content=str(ex.orig))

    async def update_course(self, course_id: int, course_in: CourseUpdate) -> tuple[Optional[Course], bool, JSONResponse]:
        try:
            course = await self.repo.update(course_id, course_in)
            await self.db.commit()
            if course:
                await self.db.refresh(course)
                return course, True, JSONResponse(status_code=HTTPStatus.OK, content={"detail": f"Course {course_id} updated"})
            return None, False, JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": f"Course {course_id} not found"})
        except IntegrityError as ex:
            await self.db.rollback()
            return None, False, JSONResponse(status_code=HTTPStatus.CONFLICT, content=str(ex.orig))

    async def delete_course(self, course_id: int) -> JSONResponse:
        try:
            course = await self.repo.delete_by_id(course_id)
            await self.db.commit()
            if course:
                return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content={"detail": f"Course {course_id} deleted"})
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"detail": f"Course {course_id} not found"})
        except IntegrityError as ex:
            await self.db.rollback()
            return JSONResponse(status_code=HTTPStatus.CONFLICT, content=str(ex.orig))

    async def add_user_to_course(self, course_id: int, user_id: int) -> CourseWithUsers:
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        user = await self.db.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        if user not in course.users:
            course.users.append(user)
            await self.db.commit()
            await self.db.refresh(course)
        await self.db.refresh(course)
        return CourseWithUsers(
            id=course.id,
            name=course.name,
            description=course.description,
            users=[u for u in course.users]
        )

    async def get_course_with_users(self, course_id: int) -> CourseWithUsers:
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        await self.db.refresh(course)
        return CourseWithUsers(
            id=course.id,
            name=course.name,
            description=course.description,
            users=[u for u in course.users]
        )

    async def remove_user_from_course(self, course_id: int, user_id: int) -> CourseWithUsers:
        course = await self.repo.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")
        user = next((u for u in course.users if u.id == user_id), None)
        if user:
            course.users.remove(user)
            await self.db.commit()
            await self.db.refresh(course)
        return CourseWithUsers(
            id=course.id,
            name=course.name,
            description=course.description,
            users=[u for u in course.users]
        )
