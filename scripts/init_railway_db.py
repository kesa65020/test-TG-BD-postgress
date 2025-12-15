"""Initialize Railway PostgreSQL database."""
import asyncio
import asyncpg

RAILWAY_URL = "postgresql://postgres:ZqSbDLoXwWuiSbZIopAfkuZywNOPoUuh@shinkansen.proxy.rlwy.net:17254/railway"

SCHEMA = """
-- Videos table
CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY,
    video_created_at TIMESTAMP,
    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,
    comments_count BIGINT DEFAULT 0,
    creator_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Video snapshots with metrics
CREATE TABLE IF NOT EXISTS video_snapshots (
    id VARCHAR(50) PRIMARY KEY,
    video_id UUID REFERENCES videos(id),
    views_count BIGINT DEFAULT 0,
    likes_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,
    comments_count BIGINT DEFAULT 0,
    delta_views_count BIGINT DEFAULT 0,
    delta_likes_count BIGINT DEFAULT 0,
    delta_reports_count BIGINT DEFAULT 0,
    delta_comments_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_snapshots_created ON video_snapshots(created_at);
CREATE INDEX IF NOT EXISTS idx_snapshots_video ON video_snapshots(video_id);
"""

async def main():
    conn = await asyncpg.connect(RAILWAY_URL)
    print("Connected to Railway PostgreSQL")
    
    await conn.execute(SCHEMA)
    print("Schema created")
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
