import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


logger = logging.getLogger(__name__)

class ErrorHandlers:
    """Handle application exceptions centrally."""

    @staticmethod
    async def handle_http_exception(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.warning(
            "HTTP error | path=%s | status=%s | detail=%s",
            request.url.path, exc.status_code, exc.detail
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail,
            },
            headers=exc.headers,
        )

    @staticmethod
    async def handle_validation_exception(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(
            "Validation error | path=%s",
            request.url.path,
        )

        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Request validation failed.",
                "errors": exc.errors(),
            },
        )

    @staticmethod
    async def handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "Unexpected error | path=%s",
            request.url.path,
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "An unexpected error occurred.",
            },
        )

    @staticmethod
    def register_handlers(app: FastAPI) -> None:
        """Register exception handlers with FastAPI."""

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
            ErrorHandlers.handle_unexpected_exception,
        )