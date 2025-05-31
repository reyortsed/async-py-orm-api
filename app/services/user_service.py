from http import HTTPStatus
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.schemas.course import CourseRead
from app.schemas.user import UserCreate, UserUpdate
from typing import Sequence, Optional
from app.models.user import User
from app.models.course import Course
from app.resources import responses
from app.schemas.user import UserWithCourses

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.db = db

    async def list_users(self) -> Sequence[User]:
        users = await self.repo.get_all()
        return users

    async def get_user(self, user_id: int) -> Optional[User]:
        user = await self.repo.get_by_id(user_id)
        return user
    
    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.repo.get_by_email(email)
        return user

    async def create_user_if_not_exists(self, user_in: UserCreate) -> tuple[User, bool, JSONResponse]:
        try:
            user = await self.repo.create(user_in)
            await self.db.commit()
            await self.db.refresh(user)
            return user, True, responses.user_created   # Created
        except IntegrityError :
            await self.db.rollback()
            existing = await self.repo.get_by_email(user_in.email)
            return existing, False, responses.user_exists  # User already exists

    async def update_user(self, user_id: int, user_in: UserUpdate) -> tuple[User, bool, JSONResponse]:
        user = None
        try:
            user = await self.repo.update(user_id, user_in)
            await self.db.commit()
            await self.db.refresh(user)
            return user, True, JSONResponse(status_code=HTTPStatus.OK,content=F"User {user_id} updated")  # Updated
        except IntegrityError as ex:
            await self.db.rollback()
            return user, False, JSONResponse(status_code=HTTPStatus.CONFLICT,content=str(ex.orig))

    async def delete_user(self, user_id: int) -> JSONResponse:
        try:
            user = await self.repo.get_by_id(user_id)
            if user is not None:
                user = await self.repo.delete_by_id(user_id)
                await self.db.commit()
                return JSONResponse(status_code=HTTPStatus.NO_CONTENT, content="User {user_id} deleted")  # Deleted
            return JSONResponse(status_code=HTTPStatus.NOT_FOUND,content=F"User {user_id} Not Found")
        except IntegrityError as ex:    
            await self.db.rollback()
            return JSONResponse(status_code=HTTPStatus.CONFLICT,content=str(ex.orig))

    async def add_course_to_user(self, user_id: int, course_id: int) -> UserWithCourses:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        course = await self.db.get(Course, course_id)
        if not course:
            raise ValueError("Course not found")
        if course not in user.courses:
            user.courses.append(course)
            await self.db.commit()
            await self.db.refresh(user)
        # Eager load courses for response
        await self.db.refresh(user)
        return UserWithCourses(
            id=user.id,
            name=user.name,
            email=user.email,
            courses=[CourseRead.model_validate(c, from_attributes=True) for c in user.courses]
        )

    async def get_user_with_courses(self, user_id: int) -> UserWithCourses:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        await self.db.refresh(user)
        return UserWithCourses(
            id=user.id,
            name=user.name,
            email=user.email,
            courses=[CourseRead.model_validate(c, from_attributes=True) for c in user.courses]
        )

    async def remove_course_from_user(self, user_id: int, course_id: int) -> UserWithCourses:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        course = next((c for c in user.courses if c.id == course_id), None)
        if course:
            user.courses.remove(course)
            await self.db.commit()
            await self.db.refresh(user)
        return UserWithCourses(
            id=user.id,
            name=user.name,
            email=user.email,
            courses=[CourseRead.model_validate(c, from_attributes=True) for c in user.courses]
        )