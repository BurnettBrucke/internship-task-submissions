import logging

from fastapi import FastAPI

from processing_service.app.api.jobs import router as jobs_router
from processing_service.app.middleware.request_id import RequestIDMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sqlalchemy import text

from processing_service.app.database import AsyncSessionLocal
from processing_service.app.queue import get_redis_pool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,
)


app = FastAPI(
    title="Processing Service",
)

app.add_middleware(RequestIDMiddleware)

app.include_router(jobs_router)

FastAPIInstrumentor.instrument_app(app)

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "processing-service",
    }


@app.get("/ready")
async def ready():
    try:
        # Check PostgreSQL
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))

        # Check Redis
        redis = await get_redis_pool()
        await redis.ping()
        await redis.aclose()

        return {
            "status": "ready",
            "service": "processing-service",
        }

    except Exception:
        return {
            "status": "not_ready",
            "service": "processing-service",
        }