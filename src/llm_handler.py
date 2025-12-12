from openai import AsyncOpenAI, APIError, APIConnectionError, APITimeoutError
from loguru import logger
from pathlib import Path

class LLMHandler:
    """Handler for LLM integration to generate SQL from natural language."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file."""
        prompt_path = Path(__file__).parent / "system_prompt.txt"
        try:
            return prompt_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            logger.error(f"System prompt file not found: {prompt_path}")
            raise
    
    async def generate_sql(self, user_query: str) -> str:
        """Generate SQL from natural language query."""
        try:
            logger.info(f"Generating SQL for query: {user_query}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0,
                max_tokens=500,
                timeout=30.0
            )
            
            sql = response.choices[0].message.content.strip()
            
            if sql.startswith('```'):
                sql = sql.split('```')[1]
                if sql.startswith('sql'):
                    sql = sql[3:]
                sql = sql.strip()
            
            logger.info(f"Generated SQL: {sql}")
            return sql
            
        except APITimeoutError:
            logger.error("LLM API timeout")
            raise Exception("LLM request timeout")
        except APIConnectionError:
            logger.error("LLM API connection error")
            raise Exception("LLM connection error")
        except APIError as e:
            logger.error(f"LLM API error: {e}")
            raise Exception(f"LLM error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in LLM handler: {e}")
            raise
