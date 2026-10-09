import json

from app.core.config import settings
from app.core.redis import get_redis_client


async def get_cache(key: str):
    redis_client = get_redis_client()

    data = await redis_client.get(key)

    if data is None:
        print("CACHE MISS:", key)
        return None

    print("CACHE HIT:", key)
    return json.loads(data)


async def set_cache(key: str, data, ttl: int | None = None):
    redis_client = get_redis_client()

    if ttl is None:
        ttl = settings.CACHE_TTL_SECONDS

    await redis_client.set(
        key,
        json.dumps(data),
        ex=ttl,
    )

    print("CACHE SET:", key)


async def delete_cache(key: str):
    redis_client = get_redis_client()

    await redis_client.delete(key)


async def invalidate_task_cache():
    redis_client = get_redis_client()

    keys = await redis_client.keys("tasks:*")

    if keys:
        await redis_client.delete(*keys)
        print("CACHE INVALIDATED:", keys)