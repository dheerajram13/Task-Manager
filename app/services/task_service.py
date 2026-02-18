from collections.abc import Callable
from datetime import date

from sqlalchemy.orm import Session

from app.api.schemas.task_request import TaskCreateRequest, TaskPatchRequest
from app.domain.entities.tag import normalize_tag_name
from app.domain.entities.task import TaskFilters
from app.domain.exceptions import NotFoundError, ValidationFailedError
from app.domain.repositories.tag_repository import TagRepository
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.db.models.task_model import TaskModel


class TaskService:
    def __init__(
        self,
        *,
        session: Session,
        task_repository: TaskRepository,
        tag_repository: TagRepository,
        today_provider: Callable[[], date],
    ) -> None:
        self._session = session
        self._task_repository = task_repository
        self._tag_repository = tag_repository
        self._today_provider = today_provider

    def create_task(self, payload: TaskCreateRequest) -> TaskModel:
        self._validate_due_date(payload.due_date)
        normalized_tags = self._normalize_tags(payload.tags)
        tags = self._tag_repository.get_or_create_many(normalized_tags)

        task = TaskModel(
            title=payload.title,
            description=payload.description,
            priority=payload.priority,
            due_date=payload.due_date,
            completed=False,
        )
        task.tags = tags

        self._task_repository.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def list_tasks(self, filters: TaskFilters) -> tuple[int, list[TaskModel]]:
        normalized_tags = self._normalize_tags(filters.tags)
        normalized_filters = TaskFilters(
            completed=filters.completed,
            priority=filters.priority,
            tags=normalized_tags,
            limit=filters.limit,
            offset=filters.offset,
        )
        total = self._task_repository.count(normalized_filters)
        items = self._task_repository.list(normalized_filters)
        return total, items

    def get_task(self, task_id: int) -> TaskModel:
        task = self._task_repository.get_by_id(task_id)
        if task is None:
            raise NotFoundError("task", task_id)
        return task

    def patch_task(self, task_id: int, payload: TaskPatchRequest) -> TaskModel:
        task = self.get_task(task_id)
        changes = payload.model_dump(exclude_unset=True)

        if not changes:
            raise ValidationFailedError({"body": "At least one field must be provided"})

        if "due_date" in changes and changes["due_date"] is not None:
            self._validate_due_date(changes["due_date"])

        if "tags" in changes:
            incoming_tags = changes.pop("tags")
            normalized_tags = self._normalize_tags(incoming_tags or [])
            task.tags = self._tag_repository.get_or_create_many(normalized_tags)

        for key, value in changes.items():
            setattr(task, key, value)

        self._session.commit()
        self._session.refresh(task)
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self._task_repository.soft_delete(task)
        self._session.commit()

    def _validate_due_date(self, due_date: date) -> None:
        if due_date < self._today_provider():
            raise ValidationFailedError({"due_date": "Must not be in the past"})

    def _normalize_tags(self, tags: list[str]) -> list[str]:
        normalized: list[str] = []
        for tag in tags:
            cleaned = normalize_tag_name(tag)
            if not cleaned:
                raise ValidationFailedError({"tags": "Tags cannot contain empty values"})
            normalized.append(cleaned)
        return list(dict.fromkeys(normalized))
