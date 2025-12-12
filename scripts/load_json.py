"""Load videos.json into PostgreSQL database."""
import json
import asyncio
import asyncpg
from pathlib import Path
from datetime import datetime


def parse_dt(val):
    """Parse ISO datetime string to datetime object (naive, no timezone)."""
    if not val:
        return None
    if isinstance(val, datetime):
        return val.replace(tzinfo=None)
    dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
    return dt.replace(tzinfo=None)


async def load_data(json_path: str, db_url: str):
    """Load JSON data into database."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    conn = await asyncpg.connect(db_url)
    
    try:
        videos = data.get("videos", [])
        print(f"Found {len(videos)} videos to load")

        for video in videos:
            # Insert video
            await conn.execute("""
                INSERT INTO videos (id, video_created_at, views_count, likes_count, 
                    reports_count, comments_count, creator_id, created_at, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (id) DO NOTHING
            """, 
                video["id"],
                parse_dt(video.get("video_created_at")),
                video.get("views_count", 0),
                video.get("likes_count", 0),
                video.get("reports_count", 0),
                video.get("comments_count", 0),
                video.get("creator_id"),
                parse_dt(video.get("created_at")),
                parse_dt(video.get("updated_at")),
            )

            # Insert snapshots
            for snap in video.get("snapshots", []):
                await conn.execute("""
                    INSERT INTO video_snapshots (id, video_id, views_count, likes_count,
                        reports_count, comments_count, delta_views_count, delta_likes_count,
                        delta_reports_count, delta_comments_count, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                    ON CONFLICT (id) DO NOTHING
                """,
                    snap["id"],
                    snap["video_id"],
                    snap.get("views_count", 0),
                    snap.get("likes_count", 0),
                    snap.get("reports_count", 0),
                    snap.get("comments_count", 0),
                    snap.get("delta_views_count", 0),
                    snap.get("delta_likes_count", 0),
                    snap.get("delta_reports_count", 0),
                    snap.get("delta_comments_count", 0),
                    parse_dt(snap.get("created_at")),
                    parse_dt(snap.get("updated_at")),
                )

        # Get counts
        video_count = await conn.fetchval("SELECT COUNT(*) FROM videos")
        snap_count = await conn.fetchval("SELECT COUNT(*) FROM video_snapshots")
        print(f"Loaded: {video_count} videos, {snap_count} snapshots")

    finally:
        await conn.close()


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    import os

    load_dotenv()
    
    json_file = sys.argv[1] if len(sys.argv) > 1 else "videos.json"
    db_url = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/video_analytics")
    
    asyncio.run(load_data(json_file, db_url))
