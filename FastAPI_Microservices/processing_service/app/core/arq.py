from arq import create_pool
from arq.connections import RedisSettings

from processing_service.app.core.config import settings


async def get_arq_pool():
    return await create_pool(
        RedisSettings(
            host="localhost",
            port=6379,
            database=0,
        )
    )