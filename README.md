# 📊 Telegram Video Analytics Bot

Telegram-бот для обработки естественноязыковых запросов о статистике видео-контента с преобразованием в SQL-запросы к PostgreSQL.

## 🎯 Возможности

- Обработка запросов на русском языке
- Преобразование текста в SQL через LLM (OpenAI API)
- Возврат числовых метрик из PostgreSQL
- Поддержка русских дат и диапазонов
- Защита от SQL-инъекций

## 📋 Требования

- Python 3.10+
- Docker & Docker Compose
- OpenAI API ключ
- Telegram Bot Token

## 🚀 Быстрый старт

### 1. Клонирование

```bash
git clone https://github.com/your-username/video-analytics-bot.git
cd video-analytics-bot
```

### 2. Настройка окружения

```bash
cp env.example .env
```

Отредактируйте `.env`:
```
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
DATABASE_URL=postgresql://user:password@localhost:5432/video_analytics
```

### 3. Запуск PostgreSQL

```bash
docker-compose up -d
```

### 4. Установка зависимостей

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### 5. Применение миграций

```bash
docker exec -i video_analytics_db psql -U user -d video_analytics -f /docker-entrypoint-initdb.d/001_init_schema.sql
```

### 6. Загрузка данных (опционально)

```bash
python scripts/load_json.py videos.json
```

### 7. Запуск бота

```bash
python bot.py
```

## 📁 Структура проекта

```
├── bot.py                  # Точка входа
├── config.py               # Конфигурация
├── requirements.txt        # Зависимости
├── env.example             # Пример .env
├── docker-compose.yml      # PostgreSQL в Docker
├── migrations/
│   └── 001_init_schema.sql # Схема БД
├── scripts/
│   └── load_json.py        # Загрузка JSON в БД
├── src/
│   ├── database.py         # Работа с PostgreSQL
│   ├── llm_handler.py      # Интеграция с OpenAI
│   ├── query_processor.py  # Валидация и выполнение SQL
│   └── system_prompt.txt   # Промпт для LLM
└── tests/
    ├── test_database.py
    ├── test_query_processor.py
    └── test_integration.py
```

## 📊 Примеры запросов

```
Сколько всего видео есть в системе?
→ 358

Сколько видео набрало больше 1000 просмотров?
→ 127

На сколько просмотров выросли все видео 28 ноября 2025?
→ 45230

Сколько разных видео получали новые просмотры 27 ноября 2025?
→ 89
```

## 🧪 Тестирование

```bash
pytest tests/ -v
```

## 🔐 Безопасность

- Валидация SQL (только SELECT)
- Блокировка опасных ключевых слов (DROP, DELETE, INSERT...)
- Read-only операции

## 📝 Лицензия

MIT
