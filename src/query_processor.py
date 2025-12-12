import re
from loguru import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import DatabaseManager
    from .llm_handler import LLMHandler

class QueryProcessor:
    """Processor for converting NL queries to SQL and executing them."""
    
    FORBIDDEN_KEYWORDS = {
        'CREATE', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER',
        'TRUNCATE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE'
    }
    
    def __init__(self, db_manager: 'DatabaseManager', llm_handler: 'LLMHandler'):
        self.db = db_manager
        self.llm = llm_handler
    
    def _validate_sql(self, sql: str) -> bool:
        """Validate SQL query for safety."""
        sql_upper = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
        sql_upper = re.sub(r'/\*.*?\*/', '', sql_upper, flags=re.DOTALL)
        sql_upper = sql_upper.upper().strip()
        
        if not sql_upper.startswith('SELECT'):
            logger.warning(f"SQL does not start with SELECT: {sql}")
            return False
        
        for keyword in self.FORBIDDEN_KEYWORDS:
            if re.search(rf'\b{keyword}\b', sql_upper):
                logger.warning(f"Forbidden keyword found: {keyword}")
                return False
        
        if not sql.strip():
            logger.warning("Empty SQL query")
            return False
        
        return True
    
    async def process(self, user_query: str) -> int:
        """Process user query and return numeric result."""
        try:
            logger.info(f"Processing query: {user_query}")
            
            sql = await self.llm.generate_sql(user_query)
            
            if not self._validate_sql(sql):
                raise Exception("Generated SQL failed validation")
            
            result = await self.db.execute_select_one(sql)
            
            logger.info(f"Query result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            raise
