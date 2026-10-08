import redis.asyncio as redis

from gateway_service.app.core.config import settings


redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


# async def test_redis_connection():
#     await redis_client.ping()
#     return True