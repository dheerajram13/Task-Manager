from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.domain.entities.task import TaskFilters
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.db.models.tag_model import TagModel
from app.infrastructure.db.models.task_model import TaskModel


class SQLTaskRepository(TaskRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, task: TaskModel) -> TaskModel:
        self._session.add(task)
        self._session.flush()
        self._session.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> TaskModel | None:
        stmt = (
            select(TaskModel)
            .options(selectinload(TaskModel.tags))
            .where(TaskModel.id == task_id)
            .where(TaskModel.deleted_at.is_(None))
        )
        return self._session.execute(stmt).scalars().first()

    def list(self, filters: TaskFilters) -> list[TaskModel]:
        stmt = self._build_base_select(filters)
        stmt = (
            stmt.options(selectinload(TaskModel.tags))
            .order_by(TaskModel.id.asc())
            .limit(filters.limit)
            .offset(filters.offset)
        )
        return list(self._session.execute(stmt).scalars().unique().all())

    def count(self, filters: TaskFilters) -> int:
        stmt = self._build_base_count(filters)
        result = self._session.execute(stmt).scalar_one()
        return int(result)

    def soft_delete(self, task: TaskModel) -> None:
        task.deleted_at = datetime.now(UTC)
        self._session.add(task)

    def _build_base_select(self, filters: TaskFilters):
        stmt = select(TaskModel).distinct()
        if filters.tags:
            stmt = stmt.join(TaskModel.tags)
        stmt = self._apply_filters(stmt, filters)
        return stmt

    def _build_base_count(self, filters: TaskFilters):
        stmt = select(func.count(func.distinct(TaskModel.id))).select_from(TaskModel)
        if filters.tags:
            stmt = stmt.join(TaskModel.tags)
        stmt = self._apply_filters(stmt, filters)
        return stmt

    def _apply_filters(self, stmt, filters: TaskFilters):
        stmt = stmt.where(TaskModel.deleted_at.is_(None))
        if filters.completed is not None:
            stmt = stmt.where(TaskModel.completed == filters.completed)
        if filters.priority is not None:
            stmt = stmt.where(TaskModel.priority == filters.priority)
        if filters.tags:
            stmt = stmt.where(TagModel.name.in_(filters.tags))
        return stmt
