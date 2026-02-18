from typing import TYPE_CHECKING

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import Base

if TYPE_CHECKING:
    from app.infrastructure.db.models.task_model import TaskModel


class TagModel(Base):
    __tablename__ = "tags"
    __table_args__ = (Index("ix_tags_name_unique", "name", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    tasks: Mapped[list["TaskModel"]] = relationship(
        "TaskModel",
        secondary="task_tags",
        back_populates="tags",
    )
