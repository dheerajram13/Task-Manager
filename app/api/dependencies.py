from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.time_provider import today
from app.infrastructure.db.session import get_db_session
from app.infrastructure.repositories.sql_tag_repository import SQLTagRepository
from app.infrastructure.repositories.sql_task_repository import SQLTaskRepository
from app.services.task_service import TaskService


def get_task_service(session: Session = Depends(get_db_session)) -> TaskService:
    return TaskService(
        session=session,
        task_repository=SQLTaskRepository(session),
        tag_repository=SQLTagRepository(session),
        today_provider=today,
    )
