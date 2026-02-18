from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    details: dict[str, str | int | float | bool | None]
