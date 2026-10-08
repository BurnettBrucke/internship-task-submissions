import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import (
    FastAPIInstrumentor,
)
from opentelemetry.instrumentation.httpx import (
    HTTPXClientInstrumentor,
)

from app.api.v1.auth import router as auth_router
from app.api.v1.jobs import router as jobs_router
from app.core.config import settings
from app.core.errors import GatewayServiceError
from app.core.logging_config import configure_logging
from app.core.request_context import get_request_id
from app.core.telemetry import configure_tracing
from app.middleware.request_context import RequestContextMiddleware

configure_tracing()

app = FastAPI(
    title="Day 8 Gateway Service",
    version="1.0.0",
)

configure_logging()

app.add_middleware(RequestContextMiddleware)


@app.exception_handler(GatewayServiceError)
async def gateway_service_error_handler(
    request,
    exc: GatewayServiceError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": get_request_id(),
            }
        },
    )


# API routers
app.include_router(auth_router)

app.include_router(
    jobs_router,
)

# OpenTelemetry instrumentation
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "gateway",
    }


@app.get("/ready")
async def ready():
    try:
        async with httpx.AsyncClient(
            base_url=settings.processing_base_url,
            timeout=2.0,
        ) as client:
            response = await client.get("/ready")

        if response.status_code == 200:
            return {
                "status": "ready",
                "service": "gateway",
                "dependencies": {
                    "processing": "ok",
                },
            }

        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "service": "gateway",
                "dependencies": {
                    "processing": "unavailable",
                },
            },
        )

    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={
                "status": "not_ready",
                "service": "gateway",
                "dependencies": {
                    "processing": "unavailable",
                },
            },
        )
