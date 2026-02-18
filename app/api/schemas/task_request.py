from datetime import date

from pydantic import BaseModel, Field, field_validator


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    priority: int = Field(..., ge=1, le=5)
    due_date: date
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title cannot be empty")
        return cleaned

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str]) -> list[str]:
        for tag in value:
            if not tag or not tag.strip():
                raise ValueError("Tags cannot contain empty values")
        return value


class TaskPatchRequest(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)
    due_date: date | None = None
    completed: bool | None = None
    tags: list[str] | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Title cannot be empty")
        return cleaned

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        for tag in value:
            if not tag or not tag.strip():
                raise ValueError("Tags cannot contain empty values")
        return value
