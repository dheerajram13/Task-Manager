from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def import_models() -> None:
    from app.infrastructure.db.models import tag_model, task_model, task_tag_model  # noqa: F401
