from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from typing import Optional, Sequence

class CourseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[Course]:
        result = await self.db.execute(select(Course))
        return result.scalars().all()

    async def get_by_id(self, course_id: int) -> Optional[Course]:
        from sqlalchemy.orm import selectinload
        from sqlalchemy.future import select
        result = await self.db.execute(
            select(Course).options(selectinload(Course.users)).where(Course.id == course_id)
        )
        return result.scalars().first()

    async def create(self, course_in: CourseCreate) -> Course:
        course = Course(**course_in.model_dump())
        self.db.add(course)
        return course

    async def update(self, course_id: int, course_in: CourseUpdate) -> Optional[Course]:
        course = await self.get_by_id(course_id)
        if not course:
            return None
        for field, value in course_in.model_dump(exclude_unset=True).items():
            setattr(course, field, value)
        return course

    async def delete_by_id(self, course_id: int) -> Optional[Course]:
        course = await self.get_by_id(course_id)
        if not course:
            return None
        await self.db.delete(course)
        return course
