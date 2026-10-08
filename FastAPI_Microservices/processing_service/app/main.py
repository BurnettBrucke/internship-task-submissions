from contextlib import asynccontextmanager

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

from sqlalchemy import text

from processing_service.app.api.jobs import router as jobs_router
from processing_service.app.core.database import engine, create_tables
from processing_service.app.core.redis import redis_client
from processing_service.app.middleware.request_id import request_id_middleware


resource = Resource.create({"service.name": "processing-service"})

tracer_provider = TracerProvider(resource=resource)

tracer_provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)

trace.set_tracer_provider(tracer_provider)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables when the service starts
    await create_tables()

    yield

    # Close database connection when the service stops
    await engine.dispose()


app = FastAPI(
    title="Processing Service",
    description="Internal processing service for Day 8 microservices project",
    version="1.0.0",
    lifespan=lifespan,
)

app.middleware("http")(request_id_middleware)


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    request_id = request.state.request_id

    error_code = "HTTP_ERROR"

    if exc.status_code == 401:
        error_code = "INVALID_SERVICE_TOKEN"

    elif exc.status_code == 403:
        error_code = "FORBIDDEN"

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


app.include_router(jobs_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "processing-service",
    }


@app.get("/ready")
async def readiness_check():
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        await redis_client.ping()

        return {
            "status": "ready",
            "service": "processing-service",
            "database": "connected",
            "redis": "connected",
        }

    except Exception:
        return {
            "status": "not_ready",
            "service": "processing-service",
            "database": "unavailable",
            "redis": "unavailable",
        }


FastAPIInstrumentor.instrument_app(app)