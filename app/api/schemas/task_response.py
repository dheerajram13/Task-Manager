from datetime import date, datetime

from pydantic import BaseModel

from app.infrastructure.db.models.task_model import TaskModel


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    due_date: date
    completed: bool
    tags: list[str]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, task: TaskModel) -> "TaskResponse":
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date,
            completed=task.completed,
            tags=[tag.name for tag in task.tags],
            created_at=task.created_at,
            updated_at=task.updated_at,
        )


class PaginatedTasksResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[TaskResponse]
