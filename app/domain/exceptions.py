from typing import Any


class AppError(Exception):
    def __init__(
        self,
        *,
        error: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(error)
        self.error = error
        self.status_code = status_code
        self.details = details or {}


class ValidationFailedError(AppError):
    def __init__(self, details: dict[str, Any]) -> None:
        super().__init__(error="Validation Failed", status_code=422, details=details)


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: Any) -> None:
        super().__init__(
            error="Not Found",
            status_code=404,
            details={resource: f"{resource} {resource_id} was not found"},
        )
