from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor,
)
from redis.asyncio import Redis
from sqlalchemy import text

from app.api.internal.jobs import router as jobs_router
from app.core.config import settings
from app.core.logging_config import configure_logging
from app.core.telemetry import configure_tracing
from app.db.session import engine
from app.middleware.request_context import RequestContextMiddleware

configure_logging()
configure_tracing()

app = FastAPI(
    title="Day 8 Processing Service",
    version="1.0.0",
)


app.add_middleware(RequestContextMiddleware)

app.include_router(jobs_router)

FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "processing",
    }


@app.get("/ready")
async def ready():

    database_status = "ok"
    redis_status = "ok"

    # Check PostgreSQL
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001
        database_status = "unavailable"

    # Check Redis
    redis_client = Redis.from_url(
        settings.redis_url,
        decode_responses=True,
    )

    try:
        await redis_client.ping()
    except Exception:  # noqa: BLE001
        redis_status = "unavailable"
    finally:
        await redis_client.aclose()

    is_ready = database_status == "ok" and redis_status == "ok"

    response = {
        "status": "ready" if is_ready else "not_ready",
        "service": "processing",
        "dependencies": {
            "database": database_status,
            "redis": redis_status,
        },
    }

    if not is_ready:
        return JSONResponse(
            status_code=503,
            content=response,
        )

    return response
