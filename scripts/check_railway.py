import asyncio
import asyncpg

async def check():
    conn = await asyncpg.connect('postgresql://postgres:ZqSbDLoXwWuiSbZIopAfkuZywNOPoUuh@shinkansen.proxy.rlwy.net:17254/railway')
    v = await conn.fetchval('SELECT COUNT(*) FROM videos')
    s = await conn.fetchval('SELECT COUNT(*) FROM video_snapshots')
    print(f'Videos: {v}, Snapshots: {s}')
    await conn.close()

asyncio.run(check())
