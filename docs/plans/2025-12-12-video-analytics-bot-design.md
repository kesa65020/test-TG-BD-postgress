# Telegram Video Analytics Bot - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Build a production-ready Telegram bot that converts Russian natural language queries about video statistics into PostgreSQL SQL and returns numeric results.

**Architecture:** 
- Telegram bot (aiogram) receives user queries in Russian
- LLM (OpenAI gpt-4o-mini) converts queries to PostgreSQL SQL
- Query processor validates SQL and executes against PostgreSQL
- Results returned as single numeric values
- Support for Russian date parsing and delta metrics

**Tech Stack:** Python 3.10+, aiogram 3.x, asyncpg, PostgreSQL 15, OpenAI API, Docker Compose

---

## Implementation Tasks (10 Total)

Each task is 2-5 minutes of work, following TDD principles.

### Task 1: Project Configuration

**Files to create:**
- config.py
- requirements.txt
- .env.example
- docker-compose.yml
- README.md
- .gitignore

**Implementation steps:**
1. Create config.py with Config class that loads environment variables
2. Create requirements.txt with all dependencies
3. Create .env.example with template variables
4. Create docker-compose.yml for PostgreSQL
5. Create comprehensive README.md
6. Create .gitignore
7. Commit: "feat: add project configuration and documentation"

### Task 2: Database Schema

**Files to create:**
- migrations/001_init_schema.sql
- migrations/002_indexes.sql

**Implementation steps:**
1. Create videos table with all required columns
2. Create video_snapshots table with delta fields
3. Create indexes for performance
4. Apply migrations to PostgreSQL
5. Commit: "feat: add database schema migrations"

### Task 3: Database Connection Manager

**Files to create:**
- src/database.py
- tests/test_db_connection.py

**Implementation steps:**
1. Create DatabaseManager class with asyncpg connection pool
2. Implement execute_query method that returns single numeric value
3. Add error handling and logging
4. Write tests for connection and query execution
5. Commit: "feat: add database connection manager"

### Task 4: Russian Date Parser

**Files to create:**
- src/date_parser.py
- tests/test_date_parser.py

**Implementation steps:**
1. Create parse_date function supporting ISO, dot format, and Russian months
2. Create parse_date_range function for date ranges
3. Support Russian month names in genitive case
4. Write comprehensive tests
5. Commit: "feat: add Russian date parser"

### Task 5: SQL Query Processor

**Files to create:**
- src/query_processor.py
- tests/test_query_processor.py

**Implementation steps:**
1. Create QueryProcessor class
2. Implement SQL validation (whitelist SELECT, block dangerous keywords)
3. Add SQL injection protection
4. Implement query execution via DatabaseManager
5. Write tests for validation and execution
6. Commit: "feat: add SQL query processor with validation"

### Task 6: LLM Handler

**Files to create:**
- src/llm_handler.py
- src/system_prompt.txt
- tests/test_llm_handler.py

**Implementation steps:**
1. Create system_prompt.txt with complete LLM instructions
2. Create LLMHandler class with OpenAI integration
3. Implement generate_sql method
4. Add error handling for API failures
5. Write tests for SQL generation
6. Commit: "feat: add LLM handler with system prompt"

### Task 7: Telegram Bot Handler

**Files to create:**
- bot.py (main file)
- tests/test_bot.py

**Implementation steps:**
1. Create bot.py with aiogram setup
2. Implement /start command handler
3. Implement message handler for queries
4. Integrate QueryProcessor
5. Add error handling with user-friendly messages
6. Write tests for bot handlers
7. Commit: "feat: add Telegram bot with query handling"

### Task 8: Bot Lifecycle and Logging

**Files to modify:**
- bot.py
- tests/test_bot_lifecycle.py

**Implementation steps:**
1. Add startup and shutdown handlers
2. Configure logging with loguru
3. Add request/response logging
4. Implement graceful shutdown
5. Write lifecycle tests
6. Commit: "feat: add bot lifecycle and logging"

### Task 9: Integration Tests

**Files to create:**
- tests/test_integration.py

**Implementation steps:**
1. Create end-to-end test: Russian query → SQL → Result
2. Test with sample data
3. Test error scenarios
4. Test date parsing in queries
5. Commit: "test: add integration tests"

### Task 10: Documentation and Final Setup

**Files to modify:**
- README.md (update with examples)
- Create .dockerignore

**Implementation steps:**
1. Add example queries and results to README
2. Add troubleshooting section
3. Create .dockerignore
4. Final verification of all components
5. Commit: "docs: finalize documentation"

---

## Execution Instructions

After plan approval, use **superpowers:subagent-driven-development** to:

1. Dispatch fresh subagent for each task
2. Review code after each task
3. Fix issues before proceeding to next task
4. Commit after each task

After all tasks complete, use **superpowers:finishing-a-development-branch** to:

1. Verify all tests pass
2. Present merge/PR options
3. Clean up worktree

