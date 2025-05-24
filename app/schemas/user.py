
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None

class UserRead(BaseModel):
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
