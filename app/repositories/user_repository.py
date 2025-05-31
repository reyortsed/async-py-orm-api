
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, Sequence

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> Sequence[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        from sqlalchemy.orm import selectinload
        from sqlalchemy.future import select
        result = await self.db.execute(
            select(User).options(selectinload(User.courses)).where(User.id == user_id)
        )
        return result.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.db.get(User, email)

    async def create(self, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        self.db.add(user)
        return user  # commit is handled by service or controller

    async def update(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        for field, value in user_in.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        return user  # commit is handled outside if using unit of work

    async def delete_by_id(self, user_id: int) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        await self.db.delete(user)
        return user
