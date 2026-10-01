import asyncio

from app.services.cache_service import (
    cache_tasks,
    get_cached_tasks,
    invalidate_tasks_cache,
)


async def main():
    user_id = 123

    test_tasks = {
        "items": [
            {
                "id": 1,
                "title": "Learn Redis",
                "description": "Understand caching",
                "priority": "high",
                "completed": False,
                "owner_id": user_id,
            }
        ],
        "page": 1,
        "page_size": 10,
        "total": 1,
    }

    print("1. Checking empty cache...")
    result = await get_cached_tasks(user_id,page=1,
    page_size=10,)
    print("Result:", result)

    print("\n2. Saving tasks to Redis...")
    await cache_tasks(
        user_id,
        page=1,
        page_size=10,
        tasks=test_tasks,
    )

    print("\n3. Reading from Redis...")
    result = await get_cached_tasks(user_id,page=1,page_size=10,)
    print("Result:", result)

    print("\n4. Invalidating cache...")
    await invalidate_tasks_cache(user_id)

    print("\n5. Checking cache after invalidation...")
    result = await get_cached_tasks(user_id,page=1,page_size=10,)
    print("Result:", result)


asyncio.run(main())