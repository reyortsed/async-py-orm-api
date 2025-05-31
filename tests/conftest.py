# tests/conftest.py

import pytest_asyncio  # ✅ needed to register async fixtures
from httpx import AsyncClient
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from main import app
from app.database import Base, get_db
from asgi_lifespan import LifespanManager
import os
from sqlalchemy.ext.asyncio import AsyncSession

from main import create_app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

app = create_app()

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocalTest = async_sessionmaker(bind=engine_test, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

async def override_get_db():
    async with AsyncSessionLocalTest() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="https://localhost") as ac:
            yield ac
