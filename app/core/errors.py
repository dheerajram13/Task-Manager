from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import get_logger
from app.domain.exceptions import AppError

logger = get_logger(__name__)


def error_payload(error: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"error": error, "details": details or {}}


def _build_validation_details(exc: RequestValidationError) -> dict[str, str]:
    details: dict[str, str] = {}
    for item in exc.errors():
        raw_loc = [str(part) for part in item.get("loc", [])]
        loc = [part for part in raw_loc if part not in {"body", "query", "path"}]
        key = ".".join(loc) if loc else "request"
        details[key] = item.get("msg", "Invalid value")
    return details or {"request": "Invalid request payload"}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload(exc.error, exc.details),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_payload("Validation Failed", _build_validation_details(exc)),
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail
        if isinstance(detail, dict) and "error" in detail and "details" in detail:
            content = detail
        elif isinstance(detail, dict):
            content = error_payload("Request Failed", detail)
        else:
            content = error_payload("Request Failed", {"message": str(detail)})
        return JSONResponse(status_code=exc.status_code, content=content)

    @app.exception_handler(Exception)
    async def handle_unexpected(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content=error_payload("Internal Server Error", {"message": "Unexpected error occurred"}),
        )
