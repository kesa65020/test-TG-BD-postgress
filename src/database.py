import asyncpg
import asyncio
from loguru import logger
from typing import Optional

class DatabaseManager:
    """Manager for PostgreSQL database operations using asyncpg."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        """Establish connection pool to PostgreSQL."""
        try:
            self.pool = await asyncpg.create_pool(
                self.database_url,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            logger.info("Database connection pool established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    async def execute_select_one(self, sql: str) -> int:
        """Execute SELECT query and return single numeric value."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        try:
            async with self.pool.acquire() as connection:
                result = await asyncio.wait_for(
                    connection.fetchval(sql),
                    timeout=30.0
                )
                if result is None:
                    return 0
                return int(result)
        except asyncio.TimeoutError:
            logger.error(f"Query timeout: {sql}")
            raise Exception("Query execution timeout")
        except Exception as e:
            logger.error(f"Query execution failed: {sql} | Error: {e}")
            raise
    
    async def close(self) -> None:
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
