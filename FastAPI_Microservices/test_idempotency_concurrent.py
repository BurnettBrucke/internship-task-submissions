import asyncio

import httpx


URL = "http://127.0.0.1:8000/api/v1/jobs"

HEADERS = {
    "Idempotency-Key": "concurrent-test-001",
}

DATA = {
    "name": "Concurrent Test",
    "job_type": "report",
    "priority": "high",
}


async def send_request(client):
    response = await client.post(
        URL,
        json=DATA,
        headers=HEADERS,
    )

    return response.status_code, response.json()


async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            send_request(client),
            send_request(client),
        )

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())