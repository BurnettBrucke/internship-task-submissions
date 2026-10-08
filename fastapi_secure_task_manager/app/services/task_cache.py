import json

from redis.exceptions import RedisError

from app.cache.redis import redis_client
from app.core.config import settings


def get_tasks_cache_key(user_id: int) -> str:
    return f"tasks:user:{user_id}"


async def get_cached_tasks(user_id: int) -> dict | None:
    key = get_tasks_cache_key(user_id)

    try:
        cached_data = await redis_client.get(key)

        if cached_data is None:
            return None

        return json.loads(cached_data)

    except RedisError:
        # Redis failure should not break the API.
        return None


async def set_cached_tasks(
    user_id: int,
    data: dict,
) -> None:
    key = get_tasks_cache_key(user_id)

    try:
        await redis_client.set(
            key,
            json.dumps(data),
            ex=settings.cache_ttl_seconds,
        )
    except RedisError:
        # Cache failure should not break the API.
        pass


async def invalidate_tasks_cache(user_id: int) -> None:
    key = get_tasks_cache_key(user_id)

    try:
        await redis_client.delete(key)
    except RedisError:
        # Cache failure should not break the API.
        pass