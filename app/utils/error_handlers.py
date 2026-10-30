import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common_schema import ErrorResponse


logger = logging.getLogger(__name__)


class ErrorHandlers:
    """Handle application exceptions centrally."""

    @staticmethod
    async def handle_http_exception(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.warning(
            "HTTP error | path=%s | status=%s | detail=%s",
            request.url.path, exc.status_code, exc.detail
        )

        response = ErrorResponse(message=str(exc.detail))
        return JSONResponse(
            status_code=exc.status_code,
            content=response.model_dump(mode="json"),
            headers=exc.headers,
        )

    @staticmethod
    async def handle_validation_exception(request: Request, exc: RequestValidationError,) -> JSONResponse:
        logger.warning(
            "Request validation failed | path=%s",
            request.url.path,
        )

        details = [
            {
                "field": ".".join(str(part) for part in error["loc"]),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]

        response = ErrorResponse(message="Request validation failed.", details=details)

        return JSONResponse(
            status_code=422,
            content=response.model_dump(mode="json"),
        )

    @staticmethod
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:

        logger.exception(
            "Unexpected error | path=%s",
            request.url.path,
        )

        response = ErrorResponse(message="An unexpected error occurred.")

        return JSONResponse(
            status_code=500,
            content=response.model_dump(mode="json"),
        )

    @staticmethod
    def register_handlers(app: FastAPI) -> None:
        app.add_exception_handler(
            StarletteHTTPException,
            ErrorHandlers.handle_http_exception,
        )

        app.add_exception_handler(
            RequestValidationError,
            ErrorHandlers.handle_validation_exception,
        )

        app.add_exception_handler(
            Exception,
            ErrorHandlers.handle_unexpected_exception
        )