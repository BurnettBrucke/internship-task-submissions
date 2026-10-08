import logging
from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.tasks import router as task_router
from app.core.config import settings
from fastapi.exceptions import RequestValidationError

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
)

from app.core.errors import (
    AppException,
    app_exception_handler,
    validation_exception_handler
)

app = FastAPI(
    title=settings.APP_NAME,
    description="Secure Task Management API",
    version="1.0.0"
)


app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }