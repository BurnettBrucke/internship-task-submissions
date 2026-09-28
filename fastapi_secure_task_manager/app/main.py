from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.errors import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(tasks_router)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {"status": "ok"}