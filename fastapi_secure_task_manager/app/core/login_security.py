from datetime import datetime, timedelta, timezone


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 10

failed_attempts = {}


def is_locked(username: str):
    record = failed_attempts.get(username)

    if record is None:
        return False

    locked_until = record.get("locked_until")

    if locked_until is None:
        return False

    if datetime.now(timezone.utc) < locked_until:
        return True

    failed_attempts.pop(username, None)
    return False

def record_failed_attempt(username: str):
    record = failed_attempts.get(
        username,
        {
            "count": 0,
            "locked_until": None
        }
    )

    record["count"] += 1

    if record["count"] >= MAX_FAILED_ATTEMPTS:
        record["locked_until"] = (
            datetime.now(timezone.utc)
            + timedelta(minutes=LOCKOUT_MINUTES)
        )

    failed_attempts[username] = record

def reset_failed_attempts(username: str):
    failed_attempts.pop(username, None)





