"""Tests for query processor module."""
import pytest
from src.query_processor import QueryProcessor


class MockDB:
    async def execute_select_one(self, sql):
        return 42


class MockLLM:
    def __init__(self, sql_response="SELECT COUNT(*) FROM videos"):
        self.sql_response = sql_response

    async def generate_sql(self, query):
        return self.sql_response


def test_validate_sql_select():
    """Test that SELECT queries pass validation."""
    processor = QueryProcessor(MockDB(), MockLLM())
    assert processor._validate_sql("SELECT COUNT(*) FROM videos") is True


def test_validate_sql_rejects_insert():
    """Test that INSERT is rejected."""
    processor = QueryProcessor(MockDB(), MockLLM())
    assert processor._validate_sql("INSERT INTO videos VALUES (1)") is False


def test_validate_sql_rejects_delete():
    """Test that DELETE is rejected."""
    processor = QueryProcessor(MockDB(), MockLLM())
    assert processor._validate_sql("DELETE FROM videos") is False


def test_validate_sql_rejects_drop():
    """Test that DROP is rejected."""
    processor = QueryProcessor(MockDB(), MockLLM())
    assert processor._validate_sql("DROP TABLE videos") is False


def test_validate_sql_rejects_update():
    """Test that UPDATE is rejected."""
    processor = QueryProcessor(MockDB(), MockLLM())
    assert processor._validate_sql("UPDATE videos SET views_count = 0") is False


def test_validate_sql_rejects_empty():
    """Test that empty SQL is rejected."""
    processor = QueryProcessor(MockDB(), MockLLM())
    assert processor._validate_sql("") is False
    assert processor._validate_sql("   ") is False


@pytest.mark.asyncio
async def test_process_returns_int():
    """Test that process returns integer result."""
    processor = QueryProcessor(MockDB(), MockLLM("SELECT COUNT(*) FROM videos"))
    result = await processor.process("Сколько видео?")
    assert result == 42


@pytest.mark.asyncio
async def test_process_rejects_dangerous_sql():
    """Test that dangerous SQL is rejected."""
    processor = QueryProcessor(MockDB(), MockLLM("DROP TABLE videos"))
    with pytest.raises(Exception, match="validation"):
        await processor.process("Удали все")
