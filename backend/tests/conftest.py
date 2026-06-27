"""
Pytest configuration and fixtures for Social Farm AI OS backend tests.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.core.database import Base, get_db


# ============================================================
# Async Event Loop
# ============================================================


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================
# Database Fixtures
# ============================================================


@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    # Use SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(test_session) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client."""
    
    async def override_get_db():
        yield test_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


# ============================================================
# Mock Fixtures
# ============================================================


@pytest.fixture
def mock_redis():
    """Create a mock Redis client."""
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock(return_value=True)
    mock.delete = AsyncMock(return_value=True)
    mock.exists = AsyncMock(return_value=False)
    return mock


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    mock = AsyncMock(spec=AsyncSession)
    mock.execute = AsyncMock()
    mock.commit = AsyncMock()
    mock.rollback = AsyncMock()
    mock.close = AsyncMock()
    return mock


# ============================================================
# Test Data Fixtures
# ============================================================


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "confirm_password": "TestPassword123!",
    }


@pytest.fixture
def sample_strategy_data():
    """Sample strategy data for testing."""
    return {
        "brand_id": "test_brand",
        "strategy_type": "monthly",
        "start_date": datetime.now(timezone.utc),
        "end_date": datetime.now(timezone.utc),
        "goals": ["Increase brand awareness", "Drive engagement"],
        "budget_usd": 10000,
        "target_platforms": ["instagram", "tiktok"],
        "target_audiences": ["farmers", "agriculture_enthusiasts"],
        "industry": "agriculture",
    }


@pytest.fixture
def sample_campaign_data():
    """Sample campaign data for testing."""
    return {
        "name": "Summer Harvest Campaign",
        "campaign_type": "product_launch",
        "start_date": datetime.now(timezone.utc),
        "end_date": datetime.now(timezone.utc),
        "objectives": [
            {"type": "awareness", "target": 100000, "metric": "impressions"},
            {"type": "engagement", "target": 5000, "metric": "likes"},
        ],
        "budget_usd": 5000,
        "target_audiences": ["farmers", "agriculture_enthusiasts"],
        "platforms": ["instagram", "tiktok"],
        "brand_id": "test_brand",
    }


@pytest.fixture
def sample_chat_messages():
    """Sample chat messages for AI testing."""
    return [
        {"role": "user", "content": "What are the best times to post on Instagram?"},
        {"role": "assistant", "content": "The best times to post on Instagram are..."},
        {"role": "user", "content": "How can I increase engagement?"},
    ]


# ============================================================
# Auth Fixtures
# ============================================================


@pytest.fixture
def auth_headers():
    """Create authentication headers with a test token."""
    from app.core.security import create_access_token
    
    token = create_access_token(subject="test_user_id")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_verify_token():
    """Mock the verify_token dependency."""
    with patch("app.core.security.verify_token") as mock:
        mock.return_value = "test_user_id"
        yield mock


# ============================================================
# Performance Fixtures
# ============================================================


@pytest.fixture
def benchmark_config():
    """Configuration for performance benchmarks."""
    return {
        "min_rounds": 10,
        "max_time": 5.0,
        "warmup_iterations": 3,
    }