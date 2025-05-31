from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from app.schemas.user import UserRead

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CourseRead(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CourseCreateResponse(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CourseWithUsers(CourseRead):
    users: List["UserRead"] = []
    model_config = ConfigDict(from_attributes=True)

from app.schemas.user import UserRead
CourseWithUsers.model_rebuild()
