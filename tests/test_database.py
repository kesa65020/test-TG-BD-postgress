"""Tests for database module."""
import pytest
import pytest_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from src.database import DatabaseManager


@pytest_asyncio.fixture
async def db():
    """Create database connection for tests."""
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/video_analytics")
    manager = DatabaseManager(db_url)
    await manager.connect()
    yield manager
    await manager.close()


@pytest.mark.asyncio
async def test_connection(db):
    """Test database connection works."""
    assert db.pool is not None


@pytest.mark.asyncio
async def test_count_videos(db):
    """Test counting videos."""
    result = await db.execute_select_one("SELECT COUNT(*) FROM videos")
    assert isinstance(result, int)
    assert result >= 0


@pytest.mark.asyncio
async def test_count_snapshots(db):
    """Test counting snapshots."""
    result = await db.execute_select_one("SELECT COUNT(*) FROM video_snapshots")
    assert isinstance(result, int)
    assert result >= 0


@pytest.mark.asyncio
async def test_sum_views(db):
    """Test summing views."""
    result = await db.execute_select_one("SELECT COALESCE(SUM(views_count), 0) FROM videos")
    assert isinstance(result, int)


@pytest.mark.asyncio
async def test_invalid_sql_raises(db):
    """Test that invalid SQL raises exception."""
    with pytest.raises(Exception):
        await db.execute_select_one("SELECT * FROM nonexistent_table")
