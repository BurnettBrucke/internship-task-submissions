import os
from urllib.parse import urlparse

from arq import create_pool
from arq.connections import RedisSettings


async def get_arq_pool():
    redis_url = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0",
    )

    parsed_url = urlparse(redis_url)

    return await create_pool(
        RedisSettings(
            host=parsed_url.hostname or "localhost",
            port=parsed_url.port or 6379,
            database=int(parsed_url.path.lstrip("/") or 0),
        )
    )