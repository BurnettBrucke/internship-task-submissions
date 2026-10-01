import json
import logging

from app.core.config import settings
from app.db.redis import get_redis_client


logger = logging.getLogger(__name__)


def get_tasks_cache_key(user_id: int, page: int, page_size: int) -> str:
    return f"tasks:user:{user_id}:page:{page}:size:{page_size}"


async def get_cached_tasks(
    user_id: int,
    page: int,
    page_size: int,
):
    redis_client = get_redis_client()

    try:
        key = get_tasks_cache_key(user_id, page, page_size)

        cached_data = await redis_client.get(key)

        if cached_data is None:
            logger.info("Redis MISS: %s", key)
            return None

        logger.info("Redis HIT: %s", key)

        return json.loads(cached_data)

    finally:
        await redis_client.aclose()


async def cache_tasks(
    user_id: int,
    page: int,
    page_size: int,
    tasks: dict,
):
    redis_client = get_redis_client()

    try:
        key = get_tasks_cache_key(user_id, page, page_size)

        await redis_client.set(
            key,
            json.dumps(tasks),
            ex=settings.CACHE_TTL_SECONDS,
        )

        logger.info(
            "Redis SET: %s (TTL=%s seconds)",
            key,
            settings.CACHE_TTL_SECONDS,
        )

    finally:
        await redis_client.aclose()


async def invalidate_tasks_cache(user_id: int):
    redis_client = get_redis_client()

    try:
        pattern = f"tasks:user:{user_id}:*"

        keys = []

        async for key in redis_client.scan_iter(match=pattern):
            keys.append(key)

        if keys:
            await redis_client.delete(*keys)

            logger.info(
                "Redis INVALIDATE: user=%s keys=%s",
                user_id,
                len(keys),
            )
        else:
            logger.info(
                "Redis INVALIDATE: user=%s no cached keys",
                user_id,
            )

    finally:
        await redis_client.aclose()