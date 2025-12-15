"""Load videos.json into Railway PostgreSQL with progress logging."""
import json
import asyncio
import asyncpg
from datetime import datetime

RAILWAY_URL = "postgresql://postgres:ZqSbDLoXwWuiSbZIopAfkuZywNOPoUuh@shinkansen.proxy.rlwy.net:17254/railway"

def parse_dt(val):
    if not val:
        return None
    if isinstance(val, datetime):
        return val.replace(tzinfo=None)
    dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
    return dt.replace(tzinfo=None)

async def load_data():
    with open("videos.json", encoding="utf-8") as f:
        data = json.load(f)

    conn = await asyncpg.connect(RAILWAY_URL)
    print(f"Connected. Loading {len(data['videos'])} videos...")

    loaded_videos = 0
    loaded_snaps = 0
    
    for i, video in enumerate(data["videos"]):
        try:
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
            loaded_videos += 1

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
                loaded_snaps += 1

            if (i + 1) % 10 == 0:
                print(f"Progress: {i+1}/{len(data['videos'])} videos, {loaded_snaps} snapshots")
                
        except Exception as e:
            print(f"Error on video {i}: {e}")
            continue

    v = await conn.fetchval('SELECT COUNT(*) FROM videos')
    s = await conn.fetchval('SELECT COUNT(*) FROM video_snapshots')
    print(f"DONE! Total in DB: {v} videos, {s} snapshots")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(load_data())
