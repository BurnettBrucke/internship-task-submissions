import asyncio

from sqlalchemy import text

from app.database import engine


async def test_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        print("Gateway database connected:", result.scalar())

    await engine.dispose()


asyncio.run(test_connection())