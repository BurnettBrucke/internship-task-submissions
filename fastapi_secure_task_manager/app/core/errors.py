from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data.",
            }
        },
    )


def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    error_codes = {
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "TASK_NOT_FOUND",
        409: "CONFLICT",
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": error_codes.get(
                    exc.status_code,
                    "HTTP_ERROR",
                ),
                "message": str(exc.detail),
            }
        },
    )