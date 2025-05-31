
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.course import CourseRead

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserCreateResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserWithCourses(UserRead):
    courses: List["CourseRead"] = []
    model_config = ConfigDict(from_attributes=True)

from app.schemas.course import CourseRead
UserWithCourses.model_rebuild()
