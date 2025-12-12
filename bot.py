import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from config import settings
from src.database import DatabaseManager
from src.llm_handler import LLMHandler
from src.query_processor import QueryProcessor

db_manager = DatabaseManager(settings.DATABASE_URL)
llm_handler = LLMHandler(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
query_processor = QueryProcessor(db_manager, llm_handler)

bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    """Handle /start command."""
    logger.info(f"User {message.from_user.id} started bot")
    await message.answer(
        "👋 Привет! Я бот для аналитики видео-контента.\n\n"
        "Отправь мне запрос на русском языке о статистике видео, "
        "и я вернул числовой результат.\n\n"
        "Примеры:\n"
        "- Сколько всего видео есть в системе?\n"
        "- Сколько видео набрало больше 100000 просмотров?\n"
        "- На сколько просмотров выросли видео 28 ноября 2025?"
    )

@dp.message()
async def query_handler(message: Message) -> None:
    """Handle user queries."""
    user_id = message.from_user.id
    query_text = message.text
    
    logger.info(f"User {user_id} sent query: {query_text}")
    
    try:
        result = await query_processor.process(query_text)
        await message.answer(f"📊 Результат: {result}")
    except Exception as e:
        logger.error(f"Error processing query from user {user_id}: {e}")
        await message.answer(
            f"❌ Ошибка при обработке запроса:\n{str(e)}\n\n"
            "Убедитесь что запрос корректен и содержит только одно числовое значение."
        )

async def main() -> None:
    """Main bot function."""
    logger.info("Starting bot...")
    
    try:
        await db_manager.connect()
        logger.info("Database connected")
        
        logger.info("Bot polling started")
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        await db_manager.close()
        await bot.session.close()
        logger.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
