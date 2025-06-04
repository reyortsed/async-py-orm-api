# tests/conftest.py
import os
import secrets
from app.common import config   
import pytest_asyncio  # ✅ needed to register async fixtures
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

# Note: 'from main import app' was here but 'app' is redefined by create_app() below.
# 'import os' was here but appears unused.
from app.database import Base, get_db
from asgi_lifespan import LifespanManager
# JWT related imports
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from main import create_app
# ... (other imports and fixtures from conftest.py) ...
# Ensure httpx is imported:
# from httpx import AsyncClient # (already there)
# Ensure settings is imported:
# from app.config import settings # (already there)

async def _fetch_azure_ad_token_client_credentials() -> str:
    print("DEBUG: Entered _fetch_azure_ad_token_client_credentials") # Add this
    """
    Fetches an Azure AD access token using the Client Credentials flow.
    Relies on TENANT_ID, CLIENT_APP_ID, CLIENT_SECRET, and API_APP_ID 
    being available in app.config.settings.
    """
    token_url = f"https://login.microsoftonline.com/{config.get_env_or_secret("TENANT_ID")}/oauth2/v2.0/token"
    
    # For Client Credentials, the scope is typically for the application's permissions to the API
    # It's often the API's App ID URI followed by /.default
    # Ensure settings.API_APP_ID is the App ID URI of your target API
    client_credentials_scope = f"{config.get_env_or_secret("API_APP_ID")}/.default" 

    data = {
        "client_id": config.get_env_or_secret("CLIENT_APP_ID"), # The ID of the client application making the request
        "client_secret": config.get_env_or_secret("CLIENT_SECRET"),
        "scope": client_credentials_scope,
        "grant_type": "client_credentials",
    }

    async with AsyncClient() as client:
        response = await client.post(token_url, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        token_data = response.json()
        if "access_token" not in token_data:
            raise ValueError("access_token not found in Azure AD response")
        return token_data["access_token"]

@pytest_asyncio.fixture
async def azure_ad_token() -> str:
    print("DEBUG: Entered azure_ad_token fixture") # Add this

    """
    Pytest fixture that provides an Azure AD access token obtained
    via the Client Credentials flow.
    """
    token = await _fetch_azure_ad_token_client_credentials()
    return token

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

app = create_app()

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocalTest = async_sessionmaker(bind=engine_test, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocalTest() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]: # Added type hint
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac: # Changed base_url
            yield ac

# Fixture factory to get an authenticated client with a provided token
@pytest_asyncio.fixture
async def get_authenticated_client(client: AsyncClient): # Depends on the existing 'client' fixture
    """
    Provides a factory function that configures the AsyncClient instance
    with a given JWT token for authentication.
    """
    def _configure_client(token: str) -> AsyncClient:
        """Sets the Authorization header on the client instance."""
        if not token or not isinstance(token, str):
            raise ValueError("A valid token string must be provided.")
        client.headers["Authorization"] = f"Bearer {token}"
        return client

    return _configure_client

