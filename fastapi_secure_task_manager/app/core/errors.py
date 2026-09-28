from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message


def unauthorized_error(
    message: str = "Authentication required",
):
    return AppException(
        status_code=401,
        code="UNAUTHORIZED",
        message=message,
    )


def forbidden_error(
    message: str = "You do not have permission",
):
    return AppException(
        status_code=403,
        code="FORBIDDEN",
        message=message,
    )


def not_found_error(
    message: str = "Resource not found",
):
    return AppException(
        status_code=404,
        code="NOT_FOUND",
        message=message,
    )


def conflict_error(
    message: str = "Resource already exists",
):
    return AppException(
        status_code=409,
        code="CONFLICT",
        message=message,
    )


# ============================================================
# CUSTOM APPLICATION EXCEPTION HANDLER
# ============================================================

async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


# ============================================================
# HTTP EXCEPTION HANDLER
# ============================================================

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    error_codes = {
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
    }

    code = error_codes.get(
        exc.status_code,
        "HTTP_ERROR",
    )

    headers = exc.headers or {}

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": str(exc.detail),
            }
        },
        headers=headers,
    )


# ============================================================
# VALIDATION ERROR HANDLER
# ============================================================

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
            }
        },
    )