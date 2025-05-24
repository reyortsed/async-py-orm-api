# app/services/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.user_service import UserService

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
