from urllib.parse import urlparse

from arq import create_pool
from arq.connections import ArqRedis, RedisSettings

from app.core.config import settings


def get_redis_settings() -> RedisSettings:
    parsed = urlparse(settings.redis_url)

    database = 0

    if parsed.path:
        database = int(parsed.path.strip("/") or "0")

    return RedisSettings(
        host=parsed.hostname or "127.0.0.1",
        port=parsed.port or 6379,
        database=database,
        username=parsed.username,
        password=parsed.password,
        ssl=parsed.scheme == "rediss",
    )


async def create_arq_pool() -> ArqRedis:
    return await create_pool(get_redis_settings())
