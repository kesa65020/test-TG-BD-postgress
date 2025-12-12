"""Integration tests - full pipeline with real DB and LLM."""
import pytest
import pytest_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from src.database import DatabaseManager
from src.llm_handler import LLMHandler
from src.query_processor import QueryProcessor


@pytest_asyncio.fixture
async def processor():
    """Create full processor with real DB and LLM."""
    db_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    
    db = DatabaseManager(db_url)
    await db.connect()
    
    llm = LLMHandler(api_key, model)
    proc = QueryProcessor(db, llm)
    
    yield proc
    
    await db.close()


@pytest.mark.asyncio
async def test_count_all_videos(processor):
    """Test: Сколько всего видео?"""
    result = await processor.process("Сколько всего видео есть в системе?")
    assert isinstance(result, int)
    assert result > 0
    print(f"Total videos: {result}")


@pytest.mark.asyncio
async def test_count_videos_with_views(processor):
    """Test: Сколько видео с просмотрами > 1000?"""
    result = await processor.process("Сколько видео набрало больше 1000 просмотров?")
    assert isinstance(result, int)
    assert result >= 0
    print(f"Videos with >1000 views: {result}")


@pytest.mark.asyncio
async def test_sum_delta_views(processor):
    """Test: Сумма прироста просмотров за дату."""
    result = await processor.process("На сколько просмотров выросли все видео 28 ноября 2025?")
    assert isinstance(result, int)
    print(f"Delta views on 28 Nov: {result}")


@pytest.mark.asyncio  
async def test_distinct_videos_with_views(processor):
    """Test: Сколько видео получали просмотры."""
    result = await processor.process("Сколько разных видео получали новые просмотры 27 ноября 2025?")
    assert isinstance(result, int)
    print(f"Videos with new views on 27 Nov: {result}")
