import hashlib
import json
import uuid

from redis.asyncio import Redis


IDEMPOTENCY_PREFIX = "idempotency:"
IN_PROGRESS_TTL = 300
COMPLETED_TTL = 86400


def _redis_key(key: str) -> str:
    return f"{IDEMPOTENCY_PREFIX}{key}"


def create_fingerprint(payload: dict) -> str:
    normalized_payload = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    return hashlib.sha256(
        normalized_payload.encode("utf-8")
    ).hexdigest()


async def get_record(
    redis: Redis,
    key: str,
) -> dict | None:

    raw = await redis.get(_redis_key(key))

    if raw is None:
        return None

    return json.loads(raw)


async def reserve_key(
    redis: Redis,
    key: str,
    fingerprint: str,
) -> str | None:

    owner = str(uuid.uuid4())

    record = {
        "state": "IN_PROGRESS",
        "fingerprint": fingerprint,
        "owner": owner,
    }

    created = await redis.set(
        _redis_key(key),
        json.dumps(record),
        nx=True,
        ex=IN_PROGRESS_TTL,
    )

    if not created:
        return None

    return owner


async def save_result(
    redis: Redis,
    key: str,
    fingerprint: str,
    job: dict,
) -> None:

    record = {
        "state": "COMPLETED",
        "fingerprint": fingerprint,
        "job": job,
    }

    await redis.set(
        _redis_key(key),
        json.dumps(record),
        ex=COMPLETED_TTL,
    )


async def release_key(
    redis: Redis,
    key: str,
    owner: str,
) -> None:

    redis_key = _redis_key(key)

    raw = await redis.get(redis_key)

    if raw is None:
        return

    record = json.loads(raw)

    if (
        record.get("state") == "IN_PROGRESS"
        and record.get("owner") == owner
    ):
        await redis.delete(redis_key)