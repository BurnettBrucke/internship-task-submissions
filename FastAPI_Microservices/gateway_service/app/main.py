from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from gateway_service.app.api.auth import router as auth_router
from gateway_service.app.api.jobs import router as jobs_router
from gateway_service.app.clients.processing_client import processing_client
from gateway_service.app.middleware.request_id import request_id_middleware


# OpenTelemetry setup
resource = Resource.create(
    {
        "service.name": "gateway-service",
    }
)

tracer_provider = TracerProvider(resource=resource)

tracer_provider.add_span_processor(
    SimpleSpanProcessor(
        ConsoleSpanExporter()
    )
)

trace.set_tracer_provider(tracer_provider)

HTTPXClientInstrumentor().instrument()


app = FastAPI(
    title="Gateway Service",
    description="Public API gateway for Day 8 microservices project",
    version="1.0.0",
)

app.middleware("http")(request_id_middleware)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    request_id = request.state.request_id

    error_code = "HTTP_ERROR"

    if exc.status_code == 409:
        error_code = "IDEMPOTENCY_CONFLICT"

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_code,
                "message": str(exc.detail),
                "request_id": request_id,
            }
        },
    )


app.include_router(auth_router)
app.include_router(jobs_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "gateway-service",
    }


@app.get("/ready")
async def readiness_check():
    try:
        processing_status = await processing_client.health_check()

        return {
            "status": "ready",
            "service": "gateway-service",
            "processing_service": processing_status,
        }

    except Exception:
        return {
            "status": "not_ready",
            "service": "gateway-service",
            "processing_service": "unavailable",
        }


FastAPIInstrumentor.instrument_app(app)