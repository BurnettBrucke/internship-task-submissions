from fastapi import Header, HTTPException, status

INTERNAL_SERVICE_TOKEN = "day8-internal-secret"


def verify_internal_service(
    authorization: str | None = Header(default=None),
):
    expected = f"Bearer {INTERNAL_SERVICE_TOKEN}"

    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid internal service credential",
        )

    return True