from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.core.errors import (
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/")
async def root():
    return {
        "message": "FastAPI Secure Task Manager is running"
    }