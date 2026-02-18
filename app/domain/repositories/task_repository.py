from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from app.domain.entities.task import TaskFilters

if TYPE_CHECKING:
    from app.infrastructure.db.models.task_model import TaskModel


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task: "TaskModel") -> "TaskModel":
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> "TaskModel | None":
        raise NotImplementedError

    @abstractmethod
    def list(self, filters: TaskFilters) -> list["TaskModel"]:
        raise NotImplementedError

    @abstractmethod
    def count(self, filters: TaskFilters) -> int:
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, task: "TaskModel") -> None:
        raise NotImplementedError
