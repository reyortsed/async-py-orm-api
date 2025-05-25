
from pydantic import BaseModel, EmailStr, ConfigDict

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
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
