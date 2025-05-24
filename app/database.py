# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # <-- connection string

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,                # ✅ explicitly declare bind
    class_= AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    session: AsyncSession = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()