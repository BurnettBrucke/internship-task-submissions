import hashlib
import json

from gateway_service.app.core.redis import redis_client


class IdempotencyService:

    def create_request_hash(
        self,
        name: str,
        job_type: str,
        priority: str,
    ) -> str:
        data = {
            "name": name,
            "job_type": job_type,
            "priority": priority,
        }

        payload = json.dumps(
            data,
            sort_keys=True,
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()

    async def get_result(self, idempotency_key: str):
        key = f"idempotency:{idempotency_key}"

        result = await redis_client.get(key)

        if result:
            return json.loads(result)

        return None

    async def save_result(
        self,
        idempotency_key: str,
        request_hash: str,
        response_data: dict,
    ):
        key = f"idempotency:{idempotency_key}"

        data = {
            "request_hash": request_hash,
            "response": response_data,
        }

        await redis_client.set(
            key,
            json.dumps(data),
            ex=86400,
        )

    async def acquire_lock(
        self,
        idempotency_key: str,
    ) -> bool:
        key = f"idempotency:lock:{idempotency_key}"

        acquired = await redis_client.set(
            key,
            "locked",
            nx=True,
            ex=60,
        )

        return acquired is True

    async def release_lock(
        self,
        idempotency_key: str,
    ):
        key = f"idempotency:lock:{idempotency_key}"

        await redis_client.delete(key)


idempotency_service = IdempotencyService()