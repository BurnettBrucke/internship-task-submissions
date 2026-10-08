from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str
    ):
        self.status_code = status_code
        self.code = code
        self.message = message


async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed."
            }
        }
    )