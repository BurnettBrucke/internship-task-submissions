import logging

from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.api.auth import router as auth_router
from app.api.jobs import router as jobs_router
from app.middleware.request_id import RequestIDMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import httpx

from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

bearer_scheme = HTTPBearer()

app = FastAPI(
    title="Gateway Service",
)

app.add_middleware(RequestIDMiddleware)

app.include_router(jobs_router)
app.include_router(auth_router)

FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "gateway-service",
    }


@app.get("/ready")
async def ready():
    try:
        # Check PostgreSQL
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))

        # Check Processing Service
        async with httpx.AsyncClient(
            timeout=2.0
        ) as client:
            response = await client.get(
                f"{settings.processing_base_url}/health"
            )

        if response.status_code != 200:
            raise RuntimeError("Processing service is not healthy")

        return {
            "status": "ready",
            "service": "gateway-service",
        }

    except Exception:
        return {
            "status": "not_ready",
            "service": "gateway-service",
        }