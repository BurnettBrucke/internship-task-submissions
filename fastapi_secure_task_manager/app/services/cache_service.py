import json

from app.core.redis import redis_client


async def get_cache(key: str):
    data = await redis_client.get(key)

    if data is None:
        print("CACHE MISS:", key)
        return None

    print("CACHE HIT:", key)
    return json.loads(data)


async def set_cache(key: str, data, ttl: int = 60):
    await redis_client.set(
        key,
        json.dumps(data),
        ex=ttl,
    )
    print("CACHE SET:", key)


async def delete_cache(key: str):
    await redis_client.delete(key)

async def invalidate_task_cache():
    keys = await redis_client.keys("tasks:*")

    if keys:
        await redis_client.delete(*keys)
        print("CACHE INVALIDATED:", keys)